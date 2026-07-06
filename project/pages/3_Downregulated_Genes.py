"""
Downregulated Genes Page
--------------------------
Displays genes meeting the downregulation criteria (adj.P.Val < 0.05, logFC <= -2).
"""

import streamlit as st
from utils.data_loader import load_downregulated, to_csv_bytes
from utils.ui_helpers import inject_global_css, page_header

st.set_page_config(page_title="Downregulated Genes | RA Dashboard", page_icon="🔻", layout="wide")
inject_global_css()

page_header(
    "Downregulated Genes",
    "Genes significantly downregulated in RA (adj.P.Val < 0.05, logFC ≤ -2).",
)

down_df = load_downregulated()

if down_df is not None:
    search_term = st.text_input("Search Gene Symbol", placeholder="e.g. ACTB, TXNIP")

    display_df = down_df.copy()
    if search_term:
        display_df = display_df[
            display_df["ID"].astype(str).str.contains(search_term, case=False, na=False)
        ]

    st.markdown(f"**{len(display_df):,}** downregulated genes shown (out of {len(down_df):,} total).")

    st.dataframe(
        display_df.sort_values("logFC", ascending=True).reset_index(drop=True),
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
        label="⬇️ Download Downregulated Genes (CSV)",
        data=to_csv_bytes(display_df),
        file_name="downregulated_genes.csv",
        mime="text/csv",
    )
