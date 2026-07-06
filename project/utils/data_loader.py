"""
data_loader.py
----------------
Utility functions for loading and validating the differential expression
CSV files used throughout the dashboard.

All data is read dynamically from disk -- nothing is hardcoded.
"""

import os
import pandas as pd
import streamlit as st

# Base data directory (relative to project root)
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")

DEG_RESULTS_PATH = os.path.join(DATA_DIR, "deg_results.csv")
UPREGULATED_PATH = os.path.join(DATA_DIR, "upregulated.csv")
DOWNREGULATED_PATH = os.path.join(DATA_DIR, "downregulated.csv")
VOLCANO_PLOT_PATH = os.path.join(ASSETS_DIR, "volcano_plot.png")


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize a raw DEG dataframe:
    - Drop stray unnamed index columns exported by R (e.g. "Unnamed: 0").
    - Ensure expected numeric columns are typed correctly.
    """
    # Drop any unnamed / empty-named index column that R writes when
    # row.names are exported (typically the first column).
    unnamed_cols = [c for c in df.columns if str(c).startswith("Unnamed") or str(c).strip() == ""]
    if unnamed_cols:
        df = df.drop(columns=unnamed_cols)

    # Coerce numeric columns
    numeric_cols = ["logFC", "AveExpr", "t", "P.Value", "adj.P.Val", "B"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df.reset_index(drop=True)


@st.cache_data(show_spinner=False)
def load_csv(path: str) -> pd.DataFrame:
    """
    Load a CSV file into a cleaned pandas DataFrame.

    Raises FileNotFoundError with a friendly message if the file is missing,
    so calling pages can display an informative Streamlit error.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Required data file not found: {os.path.basename(path)}")

    try:
        df = pd.read_csv(path)
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"Could not parse '{os.path.basename(path)}': {exc}") from exc

    return _clean_dataframe(df)


def safe_load(path: str, label: str):
    """
    Wrapper around load_csv() that surfaces a friendly Streamlit error
    instead of crashing the whole app when a file is missing or malformed.

    Returns the DataFrame, or None if loading failed (an error is already
    rendered to the page in that case).
    """
    try:
        return load_csv(path)
    except FileNotFoundError:
        st.error(
            f"⚠️ **{label} file not found.** "
            f"Please make sure the file exists at `data/{os.path.basename(path)}` "
            f"and reload the dashboard."
        )
        return None
    except ValueError as exc:
        st.error(f"⚠️ **Error reading {label}:** {exc}")
        return None


def load_deg_results() -> pd.DataFrame:
    return safe_load(DEG_RESULTS_PATH, "Differential Expression Results")


def load_upregulated() -> pd.DataFrame:
    return safe_load(UPREGULATED_PATH, "Upregulated Genes")


def load_downregulated() -> pd.DataFrame:
    return safe_load(DOWNREGULATED_PATH, "Downregulated Genes")


def count_significant(df: pd.DataFrame, alpha: float = 0.05) -> int:
    """Count genes with adj.P.Val < alpha."""
    if df is None or "adj.P.Val" not in df.columns:
        return 0
    return int((df["adj.P.Val"] < alpha).sum())


def to_csv_bytes(df: pd.DataFrame) -> bytes:
    """Convert a DataFrame to downloadable CSV bytes."""
    return df.to_csv(index=False).encode("utf-8")
