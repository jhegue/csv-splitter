"""Shared utility helpers for the CSV Splitter application."""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from app.config import DELIMITER_LABELS


_INVALID_FILENAME_PATTERN = re.compile(r'[<>:"/\\|?*\r\n\t]+')
_WHITESPACE_PATTERN = re.compile(r"\s+")


def format_count(value: int) -> str:
    """Formats an integer using periods as thousand separators.

    Args:
        value: Integer value to be formatted.

    Returns:
        A human-readable numeric string.
    """

    return f"{value:,}".replace(",", ".")


def format_delimiter(delimiter: str) -> str:
    """Returns a user-friendly label for a delimiter.

    Args:
        delimiter: Raw delimiter character.

    Returns:
        Readable delimiter label when available.
    """

    return DELIMITER_LABELS.get(delimiter, delimiter)


def sanitize_filename(value: object, used_names: set[str], extension: str) -> str:
    """Creates a unique and safe filename for an exported file.

    Args:
        value: Original group value used as filename base.
        used_names: Set of names already used in the current archive.
        extension: File extension to append to the generated filename.

    Returns:
        A safe filename including extension.
    """

    if pd.isna(value) or str(value).strip() == "":
        base_name = "sem_valor"
    else:
        base_name = str(value).strip()

    base_name = _INVALID_FILENAME_PATTERN.sub("_", base_name)
    base_name = _WHITESPACE_PATTERN.sub("_", base_name).strip("._")
    base_name = base_name or "sem_valor"

    candidate = base_name
    suffix = 2

    while candidate.lower() in used_names:
        candidate = f"{base_name}_{suffix}"
        suffix += 1

    used_names.add(candidate.lower())
    return f"{candidate}.{extension}"


def sanitize_stem(file_name: str) -> str:
    """Sanitizes a filename stem for safe ZIP output naming.

    Args:
        file_name: Original uploaded filename or arbitrary file label.

    Returns:
        A safe stem without extension.
    """

    stem = Path(file_name).stem or "arquivo"
    stem = _INVALID_FILENAME_PATTERN.sub("_", stem)
    stem = _WHITESPACE_PATTERN.sub("_", stem).strip("._")
    return stem or "arquivo"


def build_file_key(file_name: str, file_size: int, delimiter: str) -> str:
    """Builds a stable identifier for the currently uploaded file.

    Args:
        file_name: Uploaded filename.
        file_size: Uploaded file size in bytes.
        delimiter: Detected source delimiter.

    Returns:
        A stable string key used to manage Streamlit session state.
    """

    return f"{file_name}:{file_size}:{delimiter}"
