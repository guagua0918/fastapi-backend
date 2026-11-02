import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

_CODE_ROOT = Path(__file__).resolve().parents[3]


def data_root() -> Path:
    raw = os.getenv("FOOTPRINT_DATA_DIR", "").strip()
    root = Path(raw) if raw else _CODE_ROOT / "data" / "footprints"
    root.mkdir(parents=True, exist_ok=True)
    return root


def footprint_dir(mid: int, session_id: int, fid: int) -> Path:
    path = data_root() / str(mid) / str(session_id) / str(fid)
    path.mkdir(parents=True, exist_ok=True)
    return path


def relative_to_data(path: Path) -> str:
    return path.resolve().relative_to(data_root().resolve()).as_posix()


def resolve_data_path(relative: str) -> Path:
    root = data_root().resolve()
    full = (root / relative).resolve()
    if not str(full).startswith(str(root)):
        raise ValueError("path escapes data root")
    return full
