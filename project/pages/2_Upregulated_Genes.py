"""
Upregulated Genes Page
------------------------
Displays genes meeting the upregulation criteria (adj.P.Val < 0.05, logFC >= 2).
"""

import streamlit as st
from utils.data_loader import load_upregulated, to_csv_bytes
from utils.ui_helpers import inject_global_css, page_header

st.set_page_config(page_title="Upregulated Genes | RA Dashboard", page_icon="🔺", layout="wide")
inject_global_css()

page_header(
    "Upregulated Genes",
    "Genes significantly upregulated in RA (adj.P.Val < 0.05, logFC ≥ 2).",
)

up_df = load_upregulated()

if up_df is not None:
    search_term = st.text_input("Search Gene Symbol", placeholder="e.g. PDSS2, RAB39")

    display_df = up_df.copy()
    if search_term:
        display_df = display_df[
            display_df["ID"].astype(str).str.contains(search_term, case=False, na=False)
        ]

    st.markdown(f"**{len(display_df):,}** upregulated genes shown (out of {len(up_df):,} total).")

    st.dataframe(
        display_df.sort_values("logFC", ascending=False).reset_index(drop=True),
        use_container_width=True,
        height=500,
        column_config={
            "logFC": st.column_config.NumberColumn("logFC", format="%.3f"),
            "AveExpr": st.column_config.NumberColumn("AveExpr", format="%.3f"),
            "t": st.column_config.NumberColumn("t-statistic", format="%.3f"),
            "P.Value": st.column_config.NumberColumn("P-value", format="%.2e"),
            "adj.P.Val": st.column_config.NumberColumn("Adjusted P-value", format="%.2e"),
            "B": st.column_config.NumberColumn("B-statistic", format="%.3f"),
        },
    )

    st.download_button(
        label="⬇️ Download Upregulated Genes (CSV)",
        data=to_csv_bytes(display_df),
        file_name="upregulated_genes.csv",
        mime="text/csv",
    )
