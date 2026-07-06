"""
ui_helpers.py
--------------
Reusable UI components and styling helpers to keep a consistent,
publication-quality look across every page of the dashboard.
"""

import streamlit as st

# Core scientific-blue palette used throughout the dashboard
PALETTE = {
    "primary": "#1D4E89",      # deep scientific blue
    "primary_light": "#2E6DA4",
    "accent": "#5DA9E9",
    "up": "#E63946",           # red - upregulated
    "down": "#2E6DA4",         # blue - downregulated
    "neutral": "#B0B7C3",      # grey - not significant
    "background": "#FFFFFF",
    "card_bg": "#F7FAFC",
    "text": "#1B2430",
    "muted_text": "#5A6472",
}


def inject_global_css():
    """Injects the shared CSS theme (cards, typography, spacing) once per page."""
    st.markdown(
        f"""
        <style>
            /* Overall page */
            .stApp {{
                background-color: {PALETTE['background']};
                color: {PALETTE['text']};
            }}

            /* Typography */
            h1, h2, h3 {{
                font-family: 'Helvetica Neue', 'Segoe UI', sans-serif;
                color: {PALETTE['primary']};
                letter-spacing: -0.3px;
            }}
            p, li, span, label, div {{
                font-family: 'Helvetica Neue', 'Segoe UI', sans-serif;
            }}

            /* KPI Card */
            .kpi-card {{
                background-color: {PALETTE['card_bg']};
                border: 1px solid #E3E9EF;
                border-radius: 16px;
                padding: 22px 20px;
                text-align: center;
                box-shadow: 0 2px 8px rgba(29, 78, 137, 0.06);
                transition: transform 0.15s ease-in-out;
            }}
            .kpi-card:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 16px rgba(29, 78, 137, 0.12);
            }}
            .kpi-value {{
                font-size: 34px;
                font-weight: 700;
                color: {PALETTE['primary']};
                margin: 0;
            }}
            .kpi-label {{
                font-size: 14px;
                font-weight: 500;
                color: {PALETTE['muted_text']};
                margin-top: 6px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}

            /* Section card wrapper */
            .section-card {{
                background-color: {PALETTE['card_bg']};
                border-radius: 16px;
                padding: 28px;
                border: 1px solid #E3E9EF;
                margin-top: 10px;
                margin-bottom: 10px;
            }}

            /* Legend chip */
            .legend-chip {{
                display: inline-block;
                padding: 4px 14px;
                border-radius: 999px;
                font-size: 13px;
                font-weight: 600;
                color: white;
                margin-right: 8px;
            }}

            /* Sidebar */
            section[data-testid="stSidebar"] {{
                background-color: {PALETTE['card_bg']};
                border-right: 1px solid #E3E9EF;
            }}

            /* Tighten default block spacing */
            .block-container {{
                padding-top: 2rem;
                padding-bottom: 3rem;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(value, label: str) -> str:
    """Return HTML for a single KPI card."""
    return f"""
        <div class="kpi-card">
            <p class="kpi-value">{value}</p>
            <p class="kpi-label">{label}</p>
        </div>
    """


def render_kpi_row(items):
    """
    Render a row of KPI cards.
    items: list of (value, label) tuples
    """
    cols = st.columns(len(items))
    for col, (value, label) in zip(cols, items):
        with col:
            st.markdown(kpi_card(value, label), unsafe_allow_html=True)


def page_header(title: str, subtitle: str = ""):
    """Consistent page header used across all pages."""
    st.markdown(f"# {title}")
    if subtitle:
        st.markdown(
            f"<p style='color:{PALETTE['muted_text']}; font-size:16px; margin-top:-10px;'>{subtitle}</p>",
            unsafe_allow_html=True,
        )
    st.markdown("---")


def legend_chip(color: str, label: str) -> str:
    return f'<span class="legend-chip" style="background-color:{color};">{label}</span>'
