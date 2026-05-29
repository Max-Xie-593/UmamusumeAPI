from __future__ import annotations
from typing import Final

import pathlib

__all__ = (
    "CACHE_PATH",
    "UMAMUSUME_STATIC_DIR",
    "MANIFEST_PATH",
)

CACHE_PATH: Final[pathlib.Path] = pathlib.Path("./.cache/umamusume")

UMAMUSUME_STATIC_DIR: Final[str] = "umamusume"

MANIFEST_PATH: Final[str] = "manifests"
