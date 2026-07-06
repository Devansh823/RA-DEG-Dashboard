"""
Gene Search Page
-------------------
Lets the user type a gene symbol and instantly see its logFC, adjusted
P-value, average expression, and inferred regulation direction.
"""

import streamlit as st
from utils.data_loader import load_deg_results
from utils.ui_helpers import inject_global_css, page_header, render_kpi_row, PALETTE

st.set_page_config(page_title="Gene Search | RA Dashboard", page_icon="🔎", layout="wide")
inject_global_css()

page_header(
    "Gene Search",
    "Look up a specific gene symbol to see its differential expression statistics.",
)

deg_df = load_deg_results()

if deg_df is not None:
    gene_query = st.text_input(
        "Enter a Gene Symbol",
        placeholder="e.g. IL6, TNF, STAT1",
    ).strip()

    if gene_query:
        matches = deg_df[deg_df["ID"].astype(str).str.upper() == gene_query.upper()]

        if matches.empty:
            st.error("Gene not found.")
        else:
            # A gene symbol may map to multiple probes; show each match.
            for _, row in matches.iterrows():
                logfc = row["logFC"]
                adj_p = row["adj.P.Val"]
                ave_expr = row["AveExpr"]

                if logfc > 0:
                    regulation = "Upregulated"
                    reg_color = PALETTE["up"]
                elif logfc < 0:
                    regulation = "Downregulated"
                    reg_color = PALETTE["down"]
                else:
                    regulation = "No Change"
                    reg_color = PALETTE["neutral"]

                st.markdown(
                    f"""
                    <div class="section-card">
                        <h3 style="margin-top:0;">{row['ID']}</h3>
                        <span class="legend-chip" style="background-color:{reg_color};">{regulation}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                render_kpi_row(
                    [
                        (f"{logfc:.3f}", "logFC"),
                        (f"{adj_p:.2e}", "Adjusted P-value"),
                        (f"{ave_expr:.3f}", "Average Expression"),
                    ]
                )
                st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.info("Enter a gene symbol above (e.g. **IL6**, **TNF**, **STAT1**) to see its results.")
