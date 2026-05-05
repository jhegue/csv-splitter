"""Reusable Streamlit UI components."""

from __future__ import annotations

from html import escape

import pandas as pd
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from app.config import (
    APP_DESCRIPTION,
    APP_TITLE,
    DEFAULT_OUTPUT_FORMAT,
    DELIMITER_LABELS,
    OUTPUT_ARCHIVE_LABEL,
    OUTPUT_FORMATS,
    PREVIEW_HEIGHT,
    SESSION_CURRENT_FILE_KEY,
    SESSION_OUTPUT_DELIMITER_KEY,
    SESSION_OUTPUT_FORMAT_KEY,
)
from app.core import (
    build_archive,
    build_delimiter_metric_value,
    build_delivery_caption,
    build_generated_files_message,
    build_success_message,
    resolve_output_selection,
)
from app.models import ArchiveBuildResult, CsvReadResult, OutputSelection
from app.processor import read_csv_bytes
from app.utils import build_file_key, format_count, format_delimiter


def _render_section_heading(title: str, caption: str) -> None:
    """Renders a compact section heading with supporting copy."""

    st.markdown(
        f"""
        <div class="section-heading">
            <h3 class="section-heading__title">{escape(title)}</h3>
            <p class="section-heading__caption">{escape(caption)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def load_csv_document_cached(file_bytes: bytes) -> CsvReadResult:
    """Loads a CSV document with Streamlit data caching enabled.

    Args:
        file_bytes: Raw uploaded file bytes.

    Returns:
        Cached CSV read result.
    """

    return read_csv_bytes(file_bytes)


@st.cache_data(show_spinner=False)
def build_archive_cached(
    dataframe: pd.DataFrame,
    split_column: str,
    output_format: str,
    output_delimiter: str,
) -> ArchiveBuildResult:
    """Builds the downloadable archive with Streamlit data caching enabled.

    Args:
        dataframe: Already-parsed source DataFrame.
        split_column: Selected split column.
        output_format: Selected output format.
        output_delimiter: Selected output delimiter.

    Returns:
        Cached archive build result.
    """

    return build_archive(
        dataframe=dataframe,
        split_column=split_column,
        output_format=output_format,
        output_delimiter=output_delimiter,
    )


def render_header() -> None:
    """Renders the application header."""

    st.title(APP_TITLE)
    st.caption(APP_DESCRIPTION)


def render_upload_input() -> UploadedFile | None:
    """Renders the file uploader widget.

    Returns:
        Uploaded file object when a file is selected, otherwise None.
    """

    return st.file_uploader(
        "Upload CSV file",
        type="csv",
        help="The app automatically detects common delimiters such as ; , | and tab.",
    )


def render_empty_upload_state() -> None:
    """Renders the empty state shown before any upload."""

    st.info("Upload a CSV file to get started.")


def validate_dataframe(dataframe: pd.DataFrame) -> bool:
    """Validates whether the uploaded dataframe can be processed.

    Args:
        dataframe: Parsed uploaded dataframe.

    Returns:
        True when the dataframe is valid; otherwise False after rendering feedback.
    """

    if dataframe.columns.empty:
        st.error("The file does not contain any columns.")
        return False

    if dataframe.empty:
        st.warning("The file does not contain any rows.")
        return False

    return True


def initialize_output_session_state(
    uploaded_file_name: str,
    file_size: int,
    detected_delimiter: str,
) -> OutputSelection:
    """Initializes or restores output-related Streamlit session state.

    Args:
        uploaded_file_name: Uploaded file name.
        file_size: Uploaded file size in bytes.
        detected_delimiter: Detected delimiter from the source CSV.

    Returns:
        Normalized output selection for the current session.
    """

    current_file_key = build_file_key(
        file_name=uploaded_file_name,
        file_size=file_size,
        delimiter=detected_delimiter,
    )
    previous_file_key = st.session_state.get(SESSION_CURRENT_FILE_KEY)

    selection = resolve_output_selection(
        previous_file_key=previous_file_key,
        current_file_key=current_file_key,
        current_output_format=st.session_state.get(SESSION_OUTPUT_FORMAT_KEY),
        current_output_delimiter=st.session_state.get(SESSION_OUTPUT_DELIMITER_KEY),
        detected_delimiter=detected_delimiter,
    )

    st.session_state[SESSION_CURRENT_FILE_KEY] = current_file_key
    st.session_state[SESSION_OUTPUT_FORMAT_KEY] = selection.output_format
    st.session_state[SESSION_OUTPUT_DELIMITER_KEY] = selection.output_delimiter

    return selection


def render_success_feedback(read_result: CsvReadResult) -> None:
    """Renders the success feedback after a file is loaded.

    Args:
        read_result: Parsed CSV read result.
    """

    st.markdown(
        f"""
        <div class="success-banner">
            <span class="success-banner__icon">&#10003;</span>
            <div class="success-banner__text">{escape(build_success_message(read_result))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metrics_section(
    read_result: CsvReadResult,
    output_selection: OutputSelection,
) -> None:
    """Renders the top metrics section.

    Args:
        read_result: Parsed CSV read result.
        output_selection: Current output selection stored in session state.
    """

    _render_section_heading(
        "Dataset Overview",
        "A compact snapshot of the uploaded file and current export configuration.",
    )

    metrics_container = st.container()
    metric_col_1, metric_col_2, metric_col_3, metric_col_4 = metrics_container.columns(4)

    with metric_col_1:
        st.metric("Rows", format_count(len(read_result.dataframe)))

    with metric_col_2:
        st.metric("Columns", format_count(len(read_result.dataframe.columns)))

    with metric_col_3:
        st.metric(
            "Delimiter",
            build_delimiter_metric_value(
                output_format=output_selection.output_format,
                output_delimiter=output_selection.output_delimiter,
            ),
        )

    with metric_col_4:
        st.metric("Output", OUTPUT_ARCHIVE_LABEL)


def render_configuration_section(
    dataframe: pd.DataFrame,
    detected_delimiter: str,
) -> tuple[str, OutputSelection]:
    """Renders the export configuration widgets.

    Args:
        dataframe: Parsed uploaded dataframe.
        detected_delimiter: Delimiter detected from the source CSV.

    Returns:
        A tuple containing the selected split column and output configuration.
    """

    st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
    _render_section_heading(
        "Configuration",
        "Choose how the CSV should be split and how the generated files will be exported.",
    )

    config_container = st.container()
    config_col_1, config_col_2, config_col_3 = config_container.columns(3)

    with config_col_1:
        split_column = st.selectbox(
            "Split column",
            options=dataframe.columns.tolist(),
        )
        assert split_column is not None

    with config_col_2:
        output_format = st.selectbox(
            "Generated file format",
            options=list(OUTPUT_FORMATS.keys()),
            format_func=lambda key: OUTPUT_FORMATS[key]["label"],
            key=SESSION_OUTPUT_FORMAT_KEY,
        )

    with config_col_3:
        delimiter_options = list(DELIMITER_LABELS.keys())
        output_delimiter = st.selectbox(
            "Output delimiter",
            options=delimiter_options,
            format_func=format_delimiter,
            disabled=output_format != DEFAULT_OUTPUT_FORMAT,
            help="Used only when the generated format is CSV.",
            key=SESSION_OUTPUT_DELIMITER_KEY,
        )

    output_selection = OutputSelection(
        output_format=output_format,
        output_delimiter=output_delimiter
        if output_format == DEFAULT_OUTPUT_FORMAT
        else detected_delimiter,
    )

    st.caption(
        build_delivery_caption(
            output_format=output_selection.output_format,
            output_delimiter=output_selection.output_delimiter,
        )
    )

    return split_column, output_selection


def render_download_section(
    archive_result: ArchiveBuildResult,
    download_file_name: str,
    output_selection: OutputSelection,
) -> None:
    """Renders the download summary and action button.

    Args:
        archive_result: Generated archive result.
        download_file_name: Filename for the ZIP download.
        output_selection: Current output configuration.
    """

    st.divider()
    _render_section_heading(
        "Export Package",
        "Review the generated output and download the ZIP archive.",
    )
    action_col, button_col = st.columns([2.1, 1.15])

    with action_col:
        st.write(
            build_generated_files_message(
                total_files=archive_result.total_files,
                output_format=output_selection.output_format,
                output_delimiter=output_selection.output_delimiter,
            )
        )

    with button_col:
        st.download_button(
            "Download ZIP",
            data=archive_result.content,
            file_name=download_file_name,
            mime="application/zip",
            use_container_width=True,
        )


def render_preview_section(dataframe: pd.DataFrame) -> None:
    """Renders the uploaded CSV preview table.

    Args:
        dataframe: Parsed uploaded dataframe.
    """

    st.markdown('<div class="section-spacer section-spacer--lg"></div>', unsafe_allow_html=True)
    _render_section_heading(
        "Uploaded CSV Preview",
        "Inspect the first rows of the dataset before downloading the generated archive.",
    )
    st.dataframe(dataframe, use_container_width=True, height=PREVIEW_HEIGHT)
