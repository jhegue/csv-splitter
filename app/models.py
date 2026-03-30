"""Domain models used by the CSV Splitter application."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class CsvReadResult:
    """Represents the result of reading an uploaded CSV file.

    Attributes:
        dataframe: Parsed CSV content as a pandas DataFrame.
        delimiter: Detected delimiter used to read the source file.
    """

    dataframe: pd.DataFrame
    delimiter: str


@dataclass(frozen=True)
class ArchiveBuildResult:
    """Represents the generated ZIP archive.

    Attributes:
        content: Binary content of the generated ZIP file.
        total_files: Number of files written into the archive.
    """

    content: bytes
    total_files: int


@dataclass(frozen=True)
class OutputSelection:
    """Represents the current output configuration selected by the user.

    Attributes:
        output_format: Chosen format for generated files.
        output_delimiter: Delimiter used when the output format is CSV.
    """

    output_format: str
    output_delimiter: str
