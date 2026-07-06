"""
app.py
-------
Main entry point for the Rheumatoid Arthritis vs Healthy Adult
Differential Gene Expression Dashboard (GSE17755 / GPL1291).

Run with:
    streamlit run app.py
"""

import streamlit as st
from utils.data_loader import (
    load_deg_results,
    load_upregulated,
    load_downregulated,
    count_significant,
)
from utils.ui_helpers import inject_global_css, render_kpi_row, page_header, PALETTE

# ---------------------------------------------------------------------------
# Page configuration (must be the first Streamlit call)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="RA vs Healthy | DEG Dashboard",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()

# ---------------------------------------------------------------------------
# Sidebar branding (page links live automatically in the sidebar because of
# the multipage "pages/" folder convention used by Streamlit)
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🧬 GSE17755 Dashboard")
    st.markdown(
        "<span style='color:#5A6472; font-size:13px;'>Platform: GPL1291</span>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.caption("Navigate using the pages above.")

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
page_header(
    "Rheumatoid Arthritis vs Healthy Adult",
    "Differential gene expression analysis · limma (GEOquery → lmFit → eBayes → topTable)",
)

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
deg_df = load_deg_results()
up_df = load_upregulated()
down_df = load_downregulated()

# Only render KPIs/content if the core dataset loaded successfully.
if deg_df is not None:
    total_genes = len(deg_df)
    significant_genes = count_significant(deg_df, alpha=0.05)
    up_count = len(up_df) if up_df is not None else 0
    down_count = len(down_df) if down_df is not None else 0

    render_kpi_row(
        [
            (f"{total_genes:,}", "Total Genes Analysed"),
            (f"{significant_genes:,}", "Significant Genes (adj.P < 0.05)"),
            (f"{up_count:,}", "Upregulated Genes"),
            (f"{down_count:,}", "Downregulated Genes"),
        ]
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------------------------------------------------
    # Scientific explanation section
    # -----------------------------------------------------------------------
    st.markdown(
        f"""
        <div class="section-card">
        <h3 style="margin-top:0;">About This Analysis</h3>

        <p><strong>Differential Gene Expression (DGE) analysis</strong> identifies genes whose
        expression levels differ significantly between two biological conditions — in this study,
        synovial or peripheral tissue from <strong>Rheumatoid Arthritis (RA) patients</strong>
        compared with <strong>healthy adult controls</strong>. This analysis was performed using the
        <strong>limma</strong> R package, following the standard workflow of importing expression
        data via GEOquery, fitting a linear model with <code>lmFit</code>, applying empirical Bayes
        moderation with <code>eBayes</code>, and extracting ranked results with <code>topTable</code>.</p>

        <p><strong>Log Fold Change (logFC)</strong> quantifies the magnitude and direction of
        expression change between RA and healthy samples, expressed on a log2 scale. A logFC of
        +2 means a gene's expression is roughly 4-fold higher in RA samples, while a logFC of −2
        means it is roughly 4-fold lower. Genes with large positive logFC values are considered
        upregulated in disease, and large negative values are downregulated.</p>

        <p><strong>Adjusted P-value (adj.P.Val)</strong> is the statistical significance of the
        expression difference after correcting for multiple hypothesis testing (typically via the
        Benjamini–Hochberg method), which controls the false discovery rate across the thousands of
        genes tested simultaneously. A gene is generally considered <em>statistically significant</em>
        when its adjusted P-value is below 0.05, meaning there is strong evidence that the observed
        difference did not occur by chance.</p>

        <p>Together, <strong>logFC</strong> and <strong>adjusted P-value</strong> are used to define
        biologically meaningful and statistically robust up- or downregulated gene sets — the
        foundation for downstream pathway enrichment and biomarker discovery in RA research.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

else:
    st.warning(
        "The dashboard cannot display Overview metrics until `deg_results.csv` is available "
        "in the `data/` folder."
    )
