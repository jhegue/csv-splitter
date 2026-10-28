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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Streamlit-internal selectors below (data-testid, data-baseweb, [class*="css"])
   target framework internals and may break on version upgrades (tested on 1.55). */
:root {
    --surface:      rgba(255, 255, 255, 0.03);
    --surface-hi:   rgba(255, 255, 255, 0.055);
    --border:       rgba(255, 255, 255, 0.07);
    --border-hi:    rgba(255, 255, 255, 0.13);
    --border-focus: rgba(99, 102, 241, 0.5);
    --text:         #e9e9ee;
    --text-2:       #888899;
    --text-3:       #4b4b5c;
    --accent:       #6366f1;
    --success:      #34d399;
    --success-dim:  rgba(52, 211, 153, 0.07);
    --success-bdr:  rgba(52, 211, 153, 0.15);
    --r:            11px;
    --r-sm:         7px;
}

html, body, [class*="css"] {
    font-family: "Inter", system-ui, -apple-system, sans-serif;
}

.stApp { color: var(--text); }

header[data-testid="stHeader"] { display: none !important; }

.block-container {
    padding-top: 3.5rem;
    padding-bottom: 5rem;
}

h1, h2, h3 { letter-spacing: -0.03em; }

/* ─── Metric cards ─── */
div[data-testid="stMetric"] {
    padding: 1.05rem 1.15rem;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--r);
    box-shadow: none;
    transition: border-color 0.15s;
}
div[data-testid="stMetric"]:hover { border-color: var(--border-hi); }

div[data-testid="stMetricLabel"] p {
    color: var(--text-3);
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
div[data-testid="stMetricValue"] {
    color: var(--text);
    font-size: 1.5rem;
    font-weight: 600;
    line-height: 1.2;
    letter-spacing: -0.02em;
}

/* ─── File uploader ─── */
section[data-testid="stFileUploaderDropzone"] {
    border-radius: var(--r) !important;
    border: 1px dashed var(--border) !important;
    background: var(--surface) !important;
    transition: border-color 0.15s;
}
section[data-testid="stFileUploaderDropzone"]:hover {
    border-color: var(--border-hi) !important;
}
section[data-testid="stFileUploaderDropzone"] button {
    min-width: 116px;
    max-width: 148px;
    min-height: 36px;
    padding: 0.48rem 0.9rem;
    font-weight: 500 !important;
    border-radius: var(--r-sm) !important;
    border: 1px solid var(--border) !important;
    white-space: nowrap;
    flex: 0 0 auto;
    transition: border-color 0.15s;
}
section[data-testid="stFileUploaderDropzone"] button p {
    margin: 0;
    width: auto;
    text-align: center;
}

/* ─── Select boxes ─── */
div[data-baseweb="select"] > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
    transition: border-color 0.15s;
}
div[data-baseweb="select"] > div:focus-within {
    border-color: var(--border-focus) !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.08) !important;
}

/* ─── Alerts ─── */
div[data-testid="stAlert"] {
    border-radius: var(--r) !important;
    border: 1px solid var(--border) !important;
}

/* ─── Buttons ─── */
div.stButton,
div[data-testid="stDownloadButton"] { width: 100%; }

div[data-testid="stDownloadButton"] > button,
div.stButton > button {
    width: 100%;
    min-height: 40px;
    padding: 0.6rem 1rem;
    border: none !important;
    border-radius: var(--r-sm) !important;
    font-weight: 600;
    font-size: 0.875rem;
    justify-content: center;
    transition: opacity 0.15s, transform 0.12s;
}
div[data-testid="stDownloadButton"] > button {
    background: var(--accent) !important;
    color: #fff !important;
    letter-spacing: 0.01em;
}
div[data-testid="stDownloadButton"] > button:hover {
    opacity: 0.84;
    transform: translateY(-1px);
}
div.stButton > button p,
div[data-testid="stDownloadButton"] > button p {
    width: 100%;
    margin: 0;
    text-align: center;
    font-size: 0.875rem;
}

/* ─── DataFrame ─── */
div[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: var(--r);
    overflow: hidden;
}

/* ─── Divider ─── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1.5rem 0 !important;
}

/* ─── Caption ─── */
div[data-testid="stCaptionContainer"] p {
    color: var(--text-3);
    font-size: 0.775rem;
}

/* ─── Success banner ─── */
.success-banner {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    margin: 0.55rem 0 0.85rem;
    padding: 0.75rem 0.95rem;
    border-radius: var(--r);
    border: 1px solid var(--success-bdr);
    background: var(--success-dim);
    color: #a7f3d0;
}
.success-banner__icon {
    flex: 0 0 auto;
    width: 1.3rem;
    height: 1.3rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: rgba(52, 211, 153, 0.14);
    color: var(--success);
    font-size: 0.7rem;
    font-weight: 700;
}
.success-banner__text {
    font-size: 0.875rem;
    font-weight: 500;
}

/* ─── App header ─── */
.app-header { margin-bottom: 1.75rem; }
.app-header__title {
    margin: 0 0 0.3rem;
    font-size: 1.75rem;
    font-weight: 700;
    letter-spacing: -0.04em;
    color: var(--text);
    line-height: 1.1;
}
.app-header__description {
    margin: 0;
    color: var(--text-2);
    font-size: 0.875rem;
    font-weight: 400;
    line-height: 1.5;
}

/* ─── Section headings ─── */
.section-spacer     { height: 0.4rem; }
.section-spacer--lg { height: 0.8rem; }

.section-heading { margin: 1.75rem 0 0.8rem; }
.section-heading__title {
    margin: 0;
    color: var(--text);
    font-size: 0.9rem;
    font-weight: 600;
    letter-spacing: -0.005em;
}
.section-heading__caption {
    margin: 0.15rem 0 0;
    color: var(--text-2);
    font-size: 0.775rem;
    font-weight: 400;
    line-height: 1.5;
}

@media (max-width: 900px) {
    .block-container { padding-top: 2rem; }
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
