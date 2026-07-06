# RA vs Healthy Adult — Differential Gene Expression Dashboard

An interactive, publication-quality Streamlit dashboard for exploring differential
gene expression results comparing **Rheumatoid Arthritis (RA)** patients against
**Healthy Adult controls**, based on **GEO dataset GSE17755** (platform **GPL1291**).

The underlying differential expression analysis was performed in R using the
**limma** package (`GEOquery` → `lmFit` → `eBayes` → `topTable`). This dashboard
reads the resulting CSV exports and volcano plot dynamically — no hardcoded or
placeholder data is used anywhere in the app.

---

## Project Overview

| Page | Description |
|---|---|
| **Overview** | KPI summary cards + explanation of DGE, logFC, and adjusted P-value |
| **Differential Expression Results** | Full searchable/sortable/filterable gene table with CSV export |
| **Upregulated Genes** | Genes with adj.P.Val < 0.05 and logFC ≥ 2 |
| **Downregulated Genes** | Genes with adj.P.Val < 0.05 and logFC ≤ -2 |
| **Volcano Plot** | Zoomable volcano plot with color-coded legend |
| **Gene Search** | Look up any gene symbol (e.g. IL6, TNF, STAT1) for its statistics |
| **Downloads** | Direct download links for all three source CSV files |

---

## Folder Structure

```
project/
├── app.py                      # Main entry point (Overview page)
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── assets/
│   └── volcano_plot.png         # Volcano plot image (from limma analysis)
├── pages/
│   ├── 1_Differential_Expression_Results.py
│   ├── 2_Upregulated_Genes.py
│   ├── 3_Downregulated_Genes.py
│   ├── 4_Volcano_Plot.py
│   ├── 5_Gene_Search.py
│   └── 6_Downloads.py
├── utils/
│   ├── data_loader.py           # CSV loading, cleaning, caching, error handling
│   └── ui_helpers.py            # Shared CSS theme, KPI cards, page headers
└── data/
    ├── deg_results.csv          # All analyzed genes
    ├── upregulated.csv          # Significantly upregulated genes
    └── downregulated.csv        # Significantly downregulated genes
```

---

## Required Packages

- `streamlit` — dashboard framework
- `pandas` — data loading, filtering, transformation
- `plotly` — interactive charting (used for future/optional visual extensions)
- `numpy` — numerical operations
- `Pillow` — image handling for the volcano plot

All dependencies are pinned with minimum versions in `requirements.txt`.

---

## Installation

1. **Clone or download** this project folder.
2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Confirm your data files** are present in `data/` and `assets/`:
   - `data/deg_results.csv`
   - `data/upregulated.csv`
   - `data/downregulated.csv`
   - `assets/volcano_plot.png`

---

## Running the Dashboard

From the project root directory, run:

```bash
streamlit run app.py
```

Streamlit will open the dashboard automatically in your default browser
(typically at `http://localhost:8501`). Use the sidebar to navigate between
pages — Streamlit automatically builds navigation from the files in `pages/`.

---

## Features

- ✅ **100% dynamic data loading** — every table, KPI, and search result is
  computed directly from the uploaded CSV files at runtime.
- ✅ **Modern scientific theme** — white background, blue color palette,
  rounded cards, and clean publication-quality typography.
- ✅ **Interactive tables** — built-in search, column sorting, and pagination
  on every data page via Streamlit's native dataframe component.
- ✅ **Custom filters** — filter the full results table by logFC range and
  adjusted P-value threshold.
- ✅ **CSV downloads** — export filtered subsets or full raw source files.
- ✅ **Zoomable volcano plot** — slider-based zoom plus scrollable frame for
  inspecting dense regions of the plot.
- ✅ **Gene Search** — instant lookup of any gene symbol's logFC, adjusted
  P-value, average expression, and inferred regulation direction.
- ✅ **Graceful error handling** — if any required CSV or image file is
  missing or malformed, the affected page displays a clear, informative
  error instead of crashing.
- ✅ **Modular, documented codebase** — reusable utility functions for data
  loading (`utils/data_loader.py`) and UI theming (`utils/ui_helpers.py`)
  shared across all pages.

---

## Notes on Statistical Interpretation

- **logFC (log2 Fold Change)**: magnitude/direction of expression change
  between RA and Healthy Adult samples.
- **adj.P.Val (Adjusted P-value)**: Benjamini–Hochberg corrected P-value;
  values < 0.05 are considered statistically significant.
- **Upregulated genes**: adj.P.Val < 0.05 **and** logFC ≥ 2
- **Downregulated genes**: adj.P.Val < 0.05 **and** logFC ≤ -2

---

Built for academic presentations, research projects, and bioinformatics
portfolio use.
