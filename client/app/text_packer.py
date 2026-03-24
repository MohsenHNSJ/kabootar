from __future__ import annotations

import hashlib
import os
import sqlite3
import threading
import time
from pathlib import Path

try:
    from persian_encoder import PersianEncoder  # type: ignore
    from persian_encoder.seed_words import get_seed_words  # type: ignore
except Exception:  # pragma: no cover
    PersianEncoder = None  # type: ignore
    get_seed_words = None  # type: ignore


_state = threading.local()


def _encoder_db_path() -> Path | None:
    override = (os.getenv("KABOOTAR_PERSIAN_ENCODER_DB", "") or os.getenv("PERSIAN_ENCODER_DB_PATH", "")).strip()
    if override:
        return Path(override)

    seed_hash = "default"
    if get_seed_words is not None:
        try:
            payload = "\n".join(get_seed_words()).encode("utf-8")
            seed_hash = hashlib.sha1(payload).hexdigest()[:12]
        except Exception:
            seed_hash = "default"

    root = Path.home() / ".kabootar" / "client" / "persian_encoder"
    root.mkdir(parents=True, exist_ok=True)
    return root / f"lexicon-{seed_hash}.db"


def _get_engine():
    engine = getattr(_state, "engine", None)
    if engine is not None:
        return engine

    if PersianEncoder is None:
        return None

    # Use an app-owned lexicon instead of the mutable global default
    # (~/.persian_encoder/lexicon.db), otherwise server/client can decode the
    # same compact code into different words.
    last_exc: Exception | None = None
    for attempt in range(3):
        try:
            engine = PersianEncoder(
                db_path=_encoder_db_path(),
                prefer_smaller_output=True,
                size_metric="bytes",
                encode_unknown_words=False,
                ascii_only=True,
            )
            _state.engine = engine
            return engine
        except sqlite3.IntegrityError as exc:
            last_exc = exc
            if attempt >= 2:
                raise
            time.sleep(0.2 * (attempt + 1))
    if last_exc is not None:
        raise last_exc
    return None


def pack_text(value: str) -> str:
    engine = _get_engine()
    if not engine:
        return value
    return engine.encode_pack(value)


def unpack_text(value: str) -> str:
    engine = _get_engine()
    if not engine:
        return value
    return engine.decode_pack(value)
