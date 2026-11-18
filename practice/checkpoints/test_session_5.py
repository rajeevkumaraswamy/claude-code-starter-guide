"""Session 5 checkpoint: plot_sensor and the sensorlog CLI.

Run: uv run pytest checkpoints/test_session_5.py
"""

import subprocess
from pathlib import Path

import pytest

from sensorlog.load import load_csv
from sensorlog.plot import plot_sensor

ROOT = Path(__file__).resolve().parents[1]


def _run(*args):
    return subprocess.run(
        ["uv", "run", "sensorlog", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def test_plot_writes_png(tmp_path):
    df = load_csv(ROOT / "data" / "sample.csv")
    out = tmp_path / "plot.png"
    plot_sensor(df, "temp_1", out)
    assert out.read_bytes().startswith(b"\x89PNG")


def test_plot_unknown_sensor_raises(tmp_path):
    df = load_csv(ROOT / "data" / "sample.csv")
    with pytest.raises(ValueError):
        plot_sensor(df, "nope", tmp_path / "x.png")


def test_cli_summary():
    result = _run("summary", "data/sample.csv")
    assert result.returncode == 0
    lines = result.stdout.strip().splitlines()
    assert len(lines) == 3
    assert lines[0].startswith("pressure_1:")


def test_cli_missing_file():
    result = _run("summary", "data/does_not_exist.csv")
    assert result.returncode == 2
    assert result.stderr.strip()
