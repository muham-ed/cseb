"""Integration test for pipeline_v3."""
from __future__ import annotations

from pathlib import Path
from scripts.pipeline_v3 import main as run_pipeline_v3


def test_pipeline_v3_execution(tmp_path: Path):
    """Test running pipeline_v3 with count=3 end to end."""
    res = run_pipeline_v3(count=3, seed=100)
    assert res == 0
