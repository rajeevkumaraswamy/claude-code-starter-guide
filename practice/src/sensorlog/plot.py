"""Plotting helpers for sensor logs."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402


def plot_sensor(df: pd.DataFrame, sensor_id: str, out_path: Path) -> Path:
    """Write a PNG line plot of one sensor's values over time."""
    sub = df[df["sensor_id"] == sensor_id].sort_values("timestamp")
    if sub.empty:
        raise ValueError(f"unknown sensor: {sensor_id}")
    fig, ax = plt.subplots(figsize=(8, 4))
    try:
        ax.plot(sub["timestamp"], sub["value"])
        ax.set_title(sensor_id)
        ax.set_xlabel("time")
        ax.set_ylabel("value")
        fig.autofmt_xdate()
        fig.savefig(out_path, format="png")
    finally:
        plt.close(fig)
    return Path(out_path)
