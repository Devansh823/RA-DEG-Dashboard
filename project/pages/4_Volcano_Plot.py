"""
Volcano Plot Page
-------------------
Displays the pre-generated volcano_plot.png from the limma analysis,
with a simple interactive zoom control and a color legend explanation.
"""

import base64
import os
import streamlit as st
import streamlit.components.v1 as components
from utils.ui_helpers import inject_global_css, page_header, legend_chip, PALETTE
from utils.data_loader import VOLCANO_PLOT_PATH

st.set_page_config(page_title="Volcano Plot | RA Dashboard", page_icon="🌋", layout="wide")
inject_global_css()

page_header(
    "Volcano Plot",
    "logFC vs. -log10(Adjusted P-value) — generated from the limma differential expression analysis.",
)

if not os.path.exists(VOLCANO_PLOT_PATH):
    st.error(
        "⚠️ **volcano_plot.png not found.** Please make sure the file exists at "
        "`assets/volcano_plot.png` and reload the dashboard."
    )
else:
    # ---------------------------------------------------------------
    # Zoom control
    # ---------------------------------------------------------------
    zoom_pct = st.slider("🔍 Zoom", min_value=50, max_value=300, value=100, step=10, format="%d%%")

    # Encode image as base64 so it can be embedded in a scrollable HTML/CSS zoom container
    with open(VOLCANO_PLOT_PATH, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")

    components.html(
        f"""
        <div style="
            width: 100%;
            max-height: 720px;
            overflow: auto;
            border: 1px solid #E3E9EF;
            border-radius: 16px;
            background-color: #F7FAFC;
            padding: 12px;
            text-align: center;
        ">
            <img src="data:image/png;base64,{img_b64}"
                 style="width: {zoom_pct}%; height: auto; transition: width 0.15s ease-in-out;" />
        </div>
        """,
        height=760,
        scrolling=True,
    )

    st.caption("Use the zoom slider above, or scroll within the frame to inspect specific regions of the plot.")

    # ---------------------------------------------------------------
    # Legend / explanation
    # ---------------------------------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="section-card">
            <h3 style="margin-top:0;">Reading the Volcano Plot</h3>
            <p>
                {legend_chip(PALETTE['up'], 'Red')} — <strong>Upregulated genes</strong>:
                significantly higher expression in RA patients (adj.P.Val &lt; 0.05, logFC ≥ 2).
            </p>
            <p>
                {legend_chip(PALETTE['down'], 'Blue')} — <strong>Downregulated genes</strong>:
                significantly lower expression in RA patients (adj.P.Val &lt; 0.05, logFC ≤ -2).
            </p>
            <p>
                {legend_chip(PALETTE['neutral'], 'Grey')} — <strong>Not significant</strong>:
                genes that do not meet both the fold-change and adjusted P-value thresholds.
            </p>
            <p style="color:{PALETTE['muted_text']};">
                The x-axis represents log2 fold change (RA vs. Healthy Adult) and the y-axis
                represents -log10(adjusted P-value); points further from the center and higher
                up the plot indicate stronger and more statistically significant expression changes.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
