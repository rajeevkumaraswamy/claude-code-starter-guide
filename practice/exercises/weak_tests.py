"""Three deliberately weak tests for fill_missing. Do not copy their style.

Read each test and fill in the blank under it: what does it actually check,
and what bug could it never catch? (Answers are in the Session 2 guide.)
This file is for reading; it is not part of the test suite.
"""

from unittest.mock import patch

import pandas as pd
from sensorlog.clean import fill_missing


def _frame():
    return pd.DataFrame(
        {
            "timestamp": pd.to_datetime(
                ["2026-01-01 00:00", "2026-01-01 00:01", "2026-01-01 00:02"],
                utc=True,
            ),
            "sensor_id": ["a", "a", "a"],
            "value": [1.0, float("nan"), 3.0],
        }
    )


def test_runs():
    result = fill_missing(_frame())
    assert result is not None
    # 1. What does this test actually check? ________


def test_matches_itself():
    df = _frame()
    expected = fill_missing(df)
    assert fill_missing(df).equals(expected)
    # 2. What does this test actually check? ________


def test_mocked():
    with patch("sensorlog.clean.fill_missing") as fake:
        fake.return_value = _frame()
        from sensorlog import clean

        result = clean.fill_missing(_frame())
        assert result is fake.return_value
    # 3. What does this test actually check? ________
