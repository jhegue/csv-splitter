"""Application configuration constants."""

from __future__ import annotations

from typing import Final


APP_TITLE: Final[str] = "CSV Splitter"
APP_DESCRIPTION: Final[str] = (
    "Upload a CSV file, choose a column to split by, and download everything "
    "in a single ZIP."
)
PAGE_ICON: Final[str] = "🍥"
PAGE_LAYOUT: Final[str] = "wide"
INITIAL_SIDEBAR_STATE: Final[str] = "collapsed"

DEFAULT_OUTPUT_FORMAT: Final[str] = "csv"
OUTPUT_ARCHIVE_LABEL: Final[str] = "ZIP"
PREVIEW_HEIGHT: Final[int] = 360

SESSION_CURRENT_FILE_KEY: Final[str] = "current_file_key"
SESSION_OUTPUT_FORMAT_KEY: Final[str] = "output_format"
SESSION_OUTPUT_DELIMITER_KEY: Final[str] = "output_delimiter"

SUPPORTED_ENCODINGS: Final[tuple[str, ...]] = ("utf-8-sig", "utf-8", "latin1")
SUPPORTED_DELIMITERS: Final[tuple[str, ...]] = (";", ",", "\t", "|")

OUTPUT_FORMATS: Final[dict[str, dict[str, str]]] = {
    "csv": {"label": "CSV", "extension": "csv"},
    "parquet": {"label": "Parquet", "extension": "parquet"},
    "json": {"label": "JSON", "extension": "json"},
}

DELIMITER_LABELS: Final[dict[str, str]] = {
    ";": "Semicolon (;)",
    ",": "Comma (,)",
    "\t": "Tab (TSV)",
    "|": "Pipe (|)",
}
