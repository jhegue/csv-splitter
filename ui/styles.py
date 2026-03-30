"""Streamlit page configuration and visual hooks."""

from __future__ import annotations

import streamlit as st

from app.config import (
    APP_TITLE,
    INITIAL_SIDEBAR_STATE,
    PAGE_ICON,
    PAGE_LAYOUT,
)


def configure_page() -> None:
    """Configures the base Streamlit page settings."""

    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=PAGE_ICON,
        layout=PAGE_LAYOUT,
        initial_sidebar_state=INITIAL_SIDEBAR_STATE,
    )


def apply_theme_overrides() -> None:
    """Keeps the app on native Streamlit styling.

    The current version intentionally avoids custom HTML or CSS so the
    interface stays simple, maintainable, and fully Streamlit-native.
    """

