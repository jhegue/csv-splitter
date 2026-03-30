"""Streamlit entrypoint for the CSV Splitter application."""

from __future__ import annotations

import logging

import streamlit as st

from app.core import build_download_file_name
from ui.components import (
    build_archive_cached,
    initialize_output_session_state,
    load_csv_document_cached,
    render_configuration_section,
    render_download_section,
    render_empty_upload_state,
    render_header,
    render_invalid_dataframe_state,
    render_metrics_section,
    render_preview_section,
    render_success_feedback,
    render_upload_input,
)
from ui.styles import apply_theme_overrides, configure_page


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


def main() -> None:
    """Runs the Streamlit application."""
    configure_page()
    apply_theme_overrides()

    _, main_column, _ = st.columns([1, 4.6, 1])

    with main_column:
        render_header()
        uploaded_file = render_upload_input()

        if uploaded_file is None:
            render_empty_upload_state()
            return

        file_bytes = uploaded_file.getvalue()

        try:
            read_result = load_csv_document_cached(file_bytes)
        except ValueError as exc:
            st.error(str(exc))
            return

        if not render_invalid_dataframe_state(read_result.dataframe):
            return

        current_selection = initialize_output_session_state(
            uploaded_file_name=uploaded_file.name,
            file_size=len(file_bytes),
            detected_delimiter=read_result.delimiter,
        )

        render_success_feedback(read_result)
        render_metrics_section(read_result, current_selection)

        split_column, output_selection = render_configuration_section(
            dataframe=read_result.dataframe,
            detected_delimiter=read_result.delimiter,
        )

        try:
            archive_result = build_archive_cached(
                file_bytes=file_bytes,
                split_column=split_column,
                output_format=output_selection.output_format,
                output_delimiter=output_selection.output_delimiter,
            )
        except ValueError as exc:
            st.error(str(exc))
            return

        download_file_name = build_download_file_name(
            uploaded_file_name=uploaded_file.name,
            split_column=split_column,
            output_format=output_selection.output_format,
        )

        render_download_section(
            archive_result=archive_result,
            download_file_name=download_file_name,
            output_selection=output_selection,
        )
        render_preview_section(read_result.dataframe)


if __name__ == "__main__":
    main()
