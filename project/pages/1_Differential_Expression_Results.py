"""
Differential Expression Results Page
--------------------------------------
Interactive, filterable, sortable, paginated view of the full DEG results
table (deg_results.csv), with CSV download of the filtered subset.
"""

import streamlit as st
from utils.data_loader import load_deg_results, to_csv_bytes
from utils.ui_helpers import inject_global_css, page_header

st.set_page_config(page_title="DEG Results | RA Dashboard", page_icon="📊", layout="wide")
inject_global_css()

page_header(
    "Differential Expression Results",
    "Full gene list from limma topTable output — searchable, filterable, and sortable.",
)

deg_df = load_deg_results()

if deg_df is not None:
    # -------------------------------------------------------------------
    # Filters
    # -------------------------------------------------------------------
    st.markdown("#### Filters")
    filt_col1, filt_col2, filt_col3 = st.columns([2, 2, 2])

    min_lfc = float(deg_df["logFC"].min())
    max_lfc = float(deg_df["logFC"].max())

    with filt_col1:
        logfc_range = st.slider(
            "Filter by logFC range",
            min_value=round(min_lfc, 2),
            max_value=round(max_lfc, 2),
            value=(round(min_lfc, 2), round(max_lfc, 2)),
            step=0.05,
        )

    with filt_col2:
        adj_p_threshold = st.slider(
            "Filter by Adjusted P-value (≤)",
            min_value=0.0,
            max_value=1.0,
            value=1.0,
            step=0.01,
        )

    with filt_col3:
        search_term = st.text_input("Search Gene Symbol", placeholder="e.g. IL6, TNF, STAT1")

    # -------------------------------------------------------------------
    # Apply filters
    # -------------------------------------------------------------------
    filtered_df = deg_df[
        (deg_df["logFC"] >= logfc_range[0])
        & (deg_df["logFC"] <= logfc_range[1])
        & (deg_df["adj.P.Val"] <= adj_p_threshold)
    ]

    if search_term:
        filtered_df = filtered_df[
            filtered_df["ID"].astype(str).str.contains(search_term, case=False, na=False)
        ]

    st.markdown(f"**{len(filtered_df):,}** genes match the current filters (out of {len(deg_df):,} total).")

    # -------------------------------------------------------------------
    # Interactive table (built-in sorting/search/pagination via st.dataframe)
    # -------------------------------------------------------------------
    st.dataframe(
        filtered_df.sort_values("adj.P.Val").reset_index(drop=True),
        use_container_width=True,
        height=520,
        column_config={
            "logFC": st.column_config.NumberColumn("logFC", format="%.3f"),
            "AveExpr": st.column_config.NumberColumn("AveExpr", format="%.3f"),
            "t": st.column_config.NumberColumn("t-statistic", format="%.3f"),
            "P.Value": st.column_config.NumberColumn("P-value", format="%.2e"),
            "adj.P.Val": st.column_config.NumberColumn("Adjusted P-value", format="%.2e"),
            "B": st.column_config.NumberColumn("B-statistic", format="%.3f"),
        },
    )

    # -------------------------------------------------------------------
    # Download filtered results
    # -------------------------------------------------------------------
    st.download_button(
        label="⬇️ Download Filtered Table (CSV)",
        data=to_csv_bytes(filtered_df),
        file_name="filtered_deg_results.csv",
        mime="text/csv",
    )
