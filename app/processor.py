"""Low-level CSV processing functions."""

from __future__ import annotations

import csv
import io
import logging
import zipfile

import pandas as pd

from app.config import OUTPUT_FORMATS, SUPPORTED_DELIMITERS, SUPPORTED_ENCODINGS
from app.models import ArchiveBuildResult, CsvReadResult
from app.utils import sanitize_filename


logger = logging.getLogger(__name__)


def detect_delimiter(text: str) -> str:
    """Detects the delimiter used in a CSV text sample.

    Args:
        text: Raw text content of the uploaded file.

    Returns:
        The detected delimiter. Falls back to semicolon when detection fails.
    """

    sample = "\n".join(text.splitlines()[:10]).strip()

    if not sample:
        return ";"

    try:
        dialect = csv.Sniffer().sniff(sample, delimiters="".join(SUPPORTED_DELIMITERS))
        return dialect.delimiter
    except csv.Error:
        logger.debug("Delimiter detection failed. Falling back to semicolon.")
        return ";"


def read_csv_bytes(file_bytes: bytes) -> CsvReadResult:
    """Reads an uploaded CSV file from raw bytes.

    Args:
        file_bytes: Raw bytes received from the uploaded file.

    Returns:
        A parsed CSV read result containing the DataFrame and delimiter.

    Raises:
        ValueError: If the CSV cannot be decoded or parsed.
    """

    last_error: Exception | None = None

    for encoding in SUPPORTED_ENCODINGS:
        try:
            text = file_bytes.decode(encoding)
            delimiter = detect_delimiter(text)
            dataframe = pd.read_csv(io.StringIO(text), sep=delimiter)
            logger.info(
                "CSV read successfully using encoding=%s delimiter=%r.",
                encoding,
                delimiter,
            )
            return CsvReadResult(dataframe=dataframe, delimiter=delimiter)
        except UnicodeDecodeError as exc:
            last_error = exc
            logger.debug("Unable to decode CSV with encoding=%s.", encoding)
        except pd.errors.ParserError as exc:
            last_error = exc
            logger.debug("Unable to parse CSV with encoding=%s.", encoding)
        except pd.errors.EmptyDataError as exc:
            last_error = exc
            logger.debug("CSV file is empty for encoding=%s.", encoding)

    logger.error("Unable to read the uploaded CSV file.")
    raise ValueError(
        "Não foi possível ler o arquivo CSV enviado. Verifique o separador ou a codificação do arquivo."
    ) from last_error


def serialize_dataframe(
    dataframe: pd.DataFrame,
    output_format: str,
    output_delimiter: str,
) -> bytes:
    """Serializes a DataFrame to the selected output format.

    Args:
        dataframe: DataFrame to serialize.
        output_format: Output format key.
        output_delimiter: Delimiter used when exporting CSV files.

    Returns:
        Serialized binary content.

    Raises:
        ValueError: If the requested format is unsupported or unavailable.
    """

    if output_format == "csv":
        return dataframe.to_csv(sep=output_delimiter, index=False).encode("utf-8-sig")

    if output_format == "parquet":
        buffer = io.BytesIO()
        try:
            dataframe.to_parquet(buffer, index=False)
        except (ImportError, ValueError) as exc:
            logger.exception("Failed to export dataframe to parquet.")
            raise ValueError(
                "Não foi possível gerar arquivos em parquet neste ambiente."
            ) from exc

        return buffer.getvalue()

    if output_format == "json":
        return dataframe.to_json(
            orient="records",
            force_ascii=False,
            indent=2,
            date_format="iso",
        ).encode("utf-8")

    logger.error("Unsupported output format received: %s", output_format)
    raise ValueError("Formato de saída inválido.")


def build_zip_archive_from_dataframe(
    dataframe: pd.DataFrame,
    split_column: str,
    output_format: str,
    output_delimiter: str,
) -> ArchiveBuildResult:
    """Builds a ZIP archive by splitting a DataFrame on a given column.

    Args:
        dataframe: DataFrame to be split.
        split_column: Column used to create separate output files.
        output_format: Output format for generated files.
        output_delimiter: CSV delimiter for generated CSV files.

    Returns:
        The generated archive content and total number of files.

    Raises:
        ValueError: If the split column or format is invalid.
    """

    if split_column not in dataframe.columns:
        logger.error("Split column %s was not found in dataframe.", split_column)
        raise ValueError("A coluna selecionada para divisão não existe no arquivo.")

    if output_format not in OUTPUT_FORMATS:
        logger.error("Unsupported output format received: %s", output_format)
        raise ValueError("Formato de saída inválido.")

    zip_buffer = io.BytesIO()
    used_names: set[str] = set()
    total_files = 0
    extension = OUTPUT_FORMATS[output_format]["extension"]

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        for value, group in dataframe.groupby(split_column, dropna=False, sort=False):
            filtered_group = group.drop(columns=[split_column])
            file_name = sanitize_filename(value, used_names, extension)
            file_content = serialize_dataframe(
                dataframe=filtered_group,
                output_format=output_format,
                output_delimiter=output_delimiter,
            )
            archive.writestr(file_name, file_content)
            total_files += 1

    logger.info("ZIP archive built successfully with %s file(s).", total_files)
    return ArchiveBuildResult(content=zip_buffer.getvalue(), total_files=total_files)
