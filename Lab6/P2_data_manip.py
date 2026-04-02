"""
Khanon Charoenphanupong
663040475-1
P2
"""

import json
import pandas as pd
import numpy as np
import pyqtgraph as pg

from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

# ══════════════════════════════════════════════════════════════════════════
#  CONSTANTS - do not change
# ══════════════════════════════════════════════════════════════════════════

REQUIRED_COLS = {"date", "city", "temp_c", "humidity", "rainfall_mm", "condition"}
CONDITIONS    = ["Sunny", "Cloudy", "Rainy", "Stormy"]
CITIES        = ["Bangkok", "Chiang Mai", "Phuket"]


# ══════════════════════════════════════════════════════════════════════════
#  YOUR WORK — complete the 6 functions below
# ══════════════════════════════════════════════════════════════════════════

def read_csv(path: str) -> pd.DataFrame:
    """
    To do 1 — Read a CSV file and return a clean DataFrame.
    """
    df = pd.read_csv(path)

    if df.empty:
        raise ValueError("CSV file is empty.")

    if not REQUIRED_COLS.issubset(df.columns):
        missing = REQUIRED_COLS - set(df.columns)
        raise ValueError(f"Missing required columns: {missing}")

    return df


def read_json(path: str) -> pd.DataFrame:
    """
    To do 2 — Read a JSON file and return a DataFrame.
    """
    df = pd.read_json(path)

    if df.empty:
        raise ValueError("JSON file is empty.")

    if not REQUIRED_COLS.issubset(df.columns):
        missing = REQUIRED_COLS - set(df.columns)
        raise ValueError(f"Missing required columns: {missing}")

    return df


def write_csv(df: pd.DataFrame, path: str) -> None:
    """
    To do 3 — Save a DataFrame to a CSV file.
    """
    if df.empty:
        raise ValueError("DataFrame is empty. Nothing to save.")

    try:
        df.to_csv(path, index=False, encoding="utf-8")
    except Exception as e:
        raise IOError(f"Failed to write CSV: {e}")


def write_json(df: pd.DataFrame, path: str) -> None:
    """
    To do 4 — Save a DataFrame to a JSON file.
    """
    if df.empty:
        raise ValueError("DataFrame is empty. Nothing to save.")

    try:
        df.to_json(path, orient="records", indent=2, force_ascii=False)
    except Exception as e:
        raise IOError(f"Failed to write JSON: {e}")


def build_stats(df: pd.DataFrame) -> QTableWidget:
    """
    To do 5 — Return a QTableWidget showing per-city statistics.
    """
    if df.empty:
        raise ValueError("DataFrame is empty.")

    if not REQUIRED_COLS.issubset(df.columns):
        missing = REQUIRED_COLS - set(df.columns)
        raise ValueError(f"Missing required columns: {missing}")

    stats = (
        df.groupby("city")
        .agg(
            count       = ("temp_c",      "count"),
            avg_temp    = ("temp_c",      "mean"),
            max_temp    = ("temp_c",      "max"),
            min_temp    = ("temp_c",      "min"),
            total_rain  = ("rainfall_mm", "sum"),
            avg_humidity= ("humidity",    "mean"),
        )
        .round(1)
        .T  
    )

    cities_present = [c for c in CITIES if c in stats.columns]
    stats = stats[cities_present]

    row_labels = list(stats.index)
    col_labels = list(stats.columns)

    table = QTableWidget(len(row_labels), len(col_labels))
    table.setHorizontalHeaderLabels(col_labels)
    table.setVerticalHeaderLabels(row_labels)
    table.horizontalHeader().setStretchLastSection(True)
    table.setEditTriggers(QTableWidget.NoEditTriggers)
    table.setAlternatingRowColors(True)

    bold = QFont()
    bold.setBold(True)

    for ri, row_name in enumerate(row_labels):
        for ci, col_name in enumerate(col_labels):
            val = stats.loc[row_name, col_name]
            item = QTableWidgetItem(str(val))
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(ri, ci, item)

    table.resizeColumnsToContents()
    return table


def show_chart(df: pd.DataFrame, chart_type: str) -> pg.PlotWidget:
    """
    To do 6 — Draw a Rainfall Histogram chart using pyqtgraph and return a PlotWidget.
    """
    if df.empty:
        raise ValueError("DataFrame is empty.")

    if "rainfall_mm" not in df.columns:
        raise ValueError("Column 'rainfall_mm' not found in DataFrame.")

    data = df["rainfall_mm"].dropna().values

    counts, bin_edges = np.histogram(data, bins=15)

    pw = pg.PlotWidget()
    pw.setBackground("w")
    pw.setTitle("Rainfall Histogram", color="k", size="12pt")
    pw.setLabel("left",   "Frequency")
    pw.setLabel("bottom", "Rainfall (mm)")
    pw.showGrid(x=True, y=True, alpha=0.3)

    bar_width = bin_edges[1] - bin_edges[0]
    bar_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    bar = pg.BarGraphItem(
        x      = bar_centers,
        height = counts,
        width  = bar_width * 0.85,
        brush  = pg.mkBrush(74, 144, 217, 200),   
        pen    = pg.mkPen("w", width=1),
    )
    pw.addItem(bar)

    return pw