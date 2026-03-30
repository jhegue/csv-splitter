"""High-level orchestration services for the CSV Splitter application."""

from __future__ import annotations

from app.config import DEFAULT_OUTPUT_FORMAT, OUTPUT_FORMATS
from app.models import ArchiveBuildResult, CsvReadResult, OutputSelection
from app.processor import build_zip_archive_from_dataframe, read_csv_bytes
from app.utils import build_file_key, format_count, format_delimiter, sanitize_stem


def load_csv_document(file_bytes: bytes) -> CsvReadResult:
    """Reads and parses an uploaded CSV document.

    Args:
        file_bytes: Raw bytes from the uploaded file.

    Returns:
        Parsed CSV read result.
    """

    return read_csv_bytes(file_bytes)


def resolve_output_selection(
    previous_file_key: str | None,
    current_file_key: str,
    current_output_format: str | None,
    current_output_delimiter: str | None,
    detected_delimiter: str,
) -> OutputSelection:
    """Resolves the output selection to be stored in Streamlit session state.

    Args:
        previous_file_key: Previously stored file identifier.
        current_file_key: Identifier for the currently uploaded file.
        current_output_format: Current output format stored in the session.
        current_output_delimiter: Current output delimiter stored in the session.
        detected_delimiter: Delimiter detected in the uploaded CSV.

    Returns:
        A normalized output selection object.
    """

    if previous_file_key != current_file_key:
        return OutputSelection(
            output_format=DEFAULT_OUTPUT_FORMAT,
            output_delimiter=detected_delimiter,
        )

    resolved_output_format = (
        current_output_format
        if current_output_format in OUTPUT_FORMATS
        else DEFAULT_OUTPUT_FORMAT
    )
    resolved_output_delimiter = current_output_delimiter or detected_delimiter

    return OutputSelection(
        output_format=resolved_output_format,
        output_delimiter=resolved_output_delimiter,
    )


def build_file_identity(file_name: str, file_size: int, delimiter: str) -> str:
    """Builds a stable identifier for an uploaded file.

    Args:
        file_name: Uploaded filename.
        file_size: File size in bytes.
        delimiter: Detected delimiter from the source CSV.

    Returns:
        A stable identifier string.
    """

    return build_file_key(file_name=file_name, file_size=file_size, delimiter=delimiter)


def build_success_message(read_result: CsvReadResult) -> str:
    """Builds the success feedback message shown after a file is loaded.

    Args:
        read_result: Parsed CSV read result.

    Returns:
        Human-readable success message.
    """

    return (
        f"File loaded successfully: {format_count(len(read_result.dataframe))} rows "
        f"and {format_count(len(read_result.dataframe.columns))} columns."
    )


def build_delimiter_metric_value(
    output_format: str,
    output_delimiter: str,
) -> str:
    """Builds the value displayed in the delimiter metric.

    Args:
        output_format: Selected output format.
        output_delimiter: Selected output delimiter.

    Returns:
        Display value for the delimiter metric.
    """

    if output_format == "csv":
        return format_delimiter(output_delimiter)

    return "Not used"


def build_delivery_caption(output_format: str, output_delimiter: str) -> str:
    """Builds the caption shown under the configuration section.

    Args:
        output_format: Selected output format.
        output_delimiter: Selected output delimiter.

    Returns:
        Caption text for the current export configuration.
    """

    if output_format == "csv":
        return (
            "The final delivery is generated as a single ZIP file using "
            f"{format_delimiter(output_delimiter)} for CSV output."
        )

    return "The final delivery is generated as a single ZIP file."


def build_generated_files_message(
    total_files: int,
    output_format: str,
    output_delimiter: str,
) -> str:
    """Builds the summary message shown next to the download button.

    Args:
        total_files: Total number of generated files.
        output_format: Selected output format.
        output_delimiter: Selected output delimiter.

    Returns:
        User-facing generation summary.
    """

    output_label = OUTPUT_FORMATS[output_format]["label"]

    if output_format == "csv":
        return (
            f"Generated files: **{format_count(total_files)}** in **{output_label}** "
            f"using **{format_delimiter(output_delimiter)}**."
        )

    return f"Generated files: **{format_count(total_files)}** in **{output_label}**."


def build_archive(
    file_bytes: bytes,
    split_column: str,
    output_format: str,
    output_delimiter: str,
) -> ArchiveBuildResult:
    """Builds the final ZIP archive from an uploaded CSV file.

    Args:
        file_bytes: Raw uploaded file bytes.
        split_column: Column used to split the CSV.
        output_format: Selected output format.
        output_delimiter: Selected output delimiter.

    Returns:
        ZIP archive result.
    """

    read_result = load_csv_document(file_bytes)
    return build_zip_archive_from_dataframe(
        dataframe=read_result.dataframe,
        split_column=split_column,
        output_format=output_format,
        output_delimiter=output_delimiter,
    )


def build_download_file_name(
    uploaded_file_name: str,
    split_column: str,
    output_format: str,
) -> str:
    """Builds the filename used for the downloadable ZIP archive.

    Args:
        uploaded_file_name: Original uploaded filename.
        split_column: Selected split column.
        output_format: Selected output format.

    Returns:
        Safe ZIP filename for download.
    """

    return (
        f"{sanitize_stem(uploaded_file_name)}_"
        f"{sanitize_stem(split_column)}_"
        f"{OUTPUT_FORMATS[output_format]['extension']}.zip"
    )
