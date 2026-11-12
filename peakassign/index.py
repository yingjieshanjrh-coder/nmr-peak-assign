"""Finding the shift index built by nmr-novelty-check.

The predictor and the index come from the nmrcheck package, which has to be
installed (`pip install -e .` in a clone of nmr-novelty-check). The index is
only ever opened read-only.
"""
import os
from pathlib import Path

import nmrcheck
from nmrcheck.index import Index, index_path


def default_data_dir():
    """Where nmrcheck keeps its data.

    $NMRCHECK_DATA if set; otherwise the data folder next to the installed
    nmrcheck sources (that is where an editable install builds it), or
    ./data as nmrcheck itself would use.
    """
    env = os.environ.get("NMRCHECK_DATA")
    if env:
        return Path(env)
    beside = Path(nmrcheck.__file__).resolve().parent.parent / "data"
    if index_path(beside).exists():
        return beside
    return Path("data")


def open_index(data_dir=None):
    """Return nmrcheck's Index, or None when no index has been built."""
    data_dir = Path(data_dir) if data_dir else default_data_dir()
    if not index_path(data_dir).exists():
        return None
    return Index(data_dir)
