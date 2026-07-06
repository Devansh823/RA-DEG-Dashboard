"""
Downloads Page
----------------
Central location to download all raw source CSV files used by the dashboard.
"""

import os
import streamlit as st
from utils.data_loader import DEG_RESULTS_PATH, UPREGULATED_PATH, DOWNREGULATED_PATH
from utils.ui_helpers import inject_global_css, page_header

st.set_page_config(page_title="Downloads | RA Dashboard", page_icon="⬇️", layout="wide")
inject_global_css()

page_header(
    "Downloads",
    "Download the original, unfiltered source data files used throughout this dashboard.",
)


def download_file_button(path: str, label: str, file_name: str):
    """Render a download button for a file on disk, or an error if missing."""
    if not os.path.exists(path):
        st.error(f"⚠️ **{label} not found** at `{os.path.basename(path)}`.")
        return

    with open(path, "rb") as f:
        st.download_button(
            label=f"⬇️ Download {label}",
            data=f.read(),
            file_name=file_name,
            mime="text/csv",
            use_container_width=True,
        )


col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Full Results")
    st.caption("All analyzed genes from the limma differential expression analysis.")
    download_file_button(DEG_RESULTS_PATH, "deg_results.csv", "deg_results.csv")

with col2:
    st.markdown("#### Upregulated Genes")
    st.caption("adj.P.Val < 0.05 and logFC ≥ 2")
    download_file_button(UPREGULATED_PATH, "upregulated.csv", "upregulated.csv")

with col3:
    st.markdown("#### Downregulated Genes")
    st.caption("adj.P.Val < 0.05 and logFC ≤ -2")
    download_file_button(DOWNREGULATED_PATH, "downregulated.csv", "downregulated.csv")
