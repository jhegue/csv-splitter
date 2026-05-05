"""Streamlit page configuration and visual hooks."""

from __future__ import annotations

import streamlit as st

from app.config import (
    APP_TITLE,
    INITIAL_SIDEBAR_STATE,
    PAGE_ICON,
    PAGE_LAYOUT,
)


_THEME_OVERRIDES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --app-bg: #0e1117;
    --surface-0: rgba(30, 41, 59, 0.32);
    --surface-1: rgba(15, 23, 42, 0.72);
    --surface-2: rgba(37, 99, 235, 0.16);
    --border-0: rgba(148, 163, 184, 0.18);
    --border-1: rgba(59, 130, 246, 0.28);
    --text-0: #f8fafc;
    --text-1: #cbd5e1;
    --text-2: #94a3b8;
    --success-0: #22c55e;
    --success-1: rgba(34, 197, 94, 0.14);
    --blue-0: #2563eb;
    --blue-1: #1d4ed8;
    --blue-2: #60a5fa;
}

/* Streamlit-internal selectors below ([class*="css"], data-testid, data-baseweb)
   are tied to Streamlit internals and may break on version upgrades (tested on 1.55). */
html,
body,
[class*="css"] {
    font-family: "Inter", "Segoe UI", sans-serif;
}

.stApp {
    color: var(--text-0);
}

.block-container {
    padding-top: 2.25rem;
    padding-bottom: 3rem;
}

h1,
h2,
h3 {
    letter-spacing: -0.025em;
}

div[data-testid="stMetric"],
div[data-testid="stAlert"],
div[data-testid="stDataFrame"],
div[data-baseweb="select"] > div,
section[data-testid="stFileUploaderDropzone"] {
    border-radius: 18px !important;
}

div[data-baseweb="select"] > div,
section[data-testid="stFileUploaderDropzone"] {
    border: 1px solid var(--border-0) !important;
}

div[data-baseweb="select"] > div {
    background: rgba(15, 23, 42, 0.38) !important;
}

div[data-baseweb="select"] > div:focus-within {
    border-color: var(--border-1) !important;
    box-shadow: 0 0 0 1px rgba(59, 130, 246, 0.18) !important;
}

div[data-testid="stMetric"] {
    min-height: 100%;
    padding: 1rem 1.05rem;
    background:
        linear-gradient(180deg, rgba(30, 41, 59, 0.34), rgba(15, 23, 42, 0.74)),
        rgba(15, 23, 42, 0.66);
    border: 1px solid var(--border-0);
    box-shadow: 0 8px 24px rgba(2, 6, 23, 0.18);
}

div[data-testid="stMetricLabel"] p {
    color: var(--text-2);
    font-size: 0.86rem;
    font-weight: 600;
    letter-spacing: 0.01em;
}

div[data-testid="stMetricValue"] {
    color: var(--text-0);
    font-size: 1.72rem;
    font-weight: 700;
    line-height: 1.1;
}

div[data-testid="stDownloadButton"] {
    width: 100%;
}

div.stButton,
div[data-testid="stDownloadButton"] {
    width: 100%;
}

div.stButton > button,
div[data-testid="stDownloadButton"] > button {
    width: 100%;
    min-height: 46px;
    padding: 0.75rem 1rem;
    border: none !important;
    border-radius: 8px !important;
    text-align: center;
    justify-content: center;
    transition: all 0.3s ease;
}

div[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, var(--blue-0), var(--blue-1));
    color: #ffffff;
    font-weight: 700;
    box-shadow: 0 12px 26px rgba(37, 99, 235, 0.28);
}

div[data-testid="stDownloadButton"] > button:hover {
    transform: translateY(-1px);
    filter: brightness(1.05);
    box-shadow: 0 14px 30px rgba(37, 99, 235, 0.34);
}

div.stButton > button p,
div[data-testid="stDownloadButton"] > button p {
    width: 100%;
    margin: 0;
    text-align: center;
}

div[data-testid="stDownloadButton"] > button p {
    font-size: 0.98rem;
}

section[data-testid="stFileUploaderDropzone"] button,
div.stButton > button {
    font-weight: 600;
}

section[data-testid="stFileUploaderDropzone"] button {
    width: fit-content !important;
    min-width: 132px;
    max-width: 156px;
    min-height: 42px;
    padding: 0.65rem 1rem;
    border: none !important;
    border-radius: 8px !important;
    white-space: nowrap;
    flex: 0 0 auto;
    transition: all 0.3s ease;
}

section[data-testid="stFileUploaderDropzone"] button p {
    width: auto;
    margin: 0;
    text-align: center;
}

div[data-testid="stAlert"] {
    border: 1px solid var(--border-0);
}

.success-banner {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin: 0.85rem 0 1rem;
    padding: 1rem 1.1rem;
    border-radius: 18px;
    border: 1px solid rgba(34, 197, 94, 0.22);
    background:
        linear-gradient(180deg, rgba(34, 197, 94, 0.12), rgba(21, 128, 61, 0.08)),
        rgba(15, 23, 42, 0.42);
    color: #dcfce7;
    box-shadow: 0 10px 28px rgba(21, 128, 61, 0.12);
}

.success-banner__icon {
    flex: 0 0 auto;
    width: 2rem;
    height: 2rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 999px;
    background: var(--success-1);
    color: #86efac;
    font-size: 1rem;
    font-weight: 800;
}

.success-banner__text {
    font-size: 1rem;
    font-weight: 600;
    line-height: 1.5;
}

.section-spacer {
    height: 1rem;
}

.section-spacer--lg {
    height: 1.45rem;
}

.section-heading {
    margin: 1.4rem 0 0.8rem;
}

.section-heading__title {
    margin: 0;
    color: var(--text-0);
    font-size: 1.1rem;
    font-weight: 700;
}

.section-heading__caption {
    margin: 0.3rem 0 0;
    color: var(--text-2);
    font-size: 0.9rem;
}

div[data-testid="stDataFrame"] {
    border: 1px solid var(--border-0);
    overflow: hidden;
}

@media (max-width: 900px) {
    .block-container {
        padding-top: 1.6rem;
    }
}
</style>
"""


def configure_page() -> None:
    """Configures the base Streamlit page settings."""

    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=PAGE_ICON,
        layout=PAGE_LAYOUT,
        initial_sidebar_state=INITIAL_SIDEBAR_STATE,
    )


def apply_theme_overrides() -> None:
    """Applies lightweight UI refinements to the native Streamlit layout."""

    st.markdown(_THEME_OVERRIDES, unsafe_allow_html=True)
