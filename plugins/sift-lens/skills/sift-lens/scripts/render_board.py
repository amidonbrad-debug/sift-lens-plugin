"""Render an actual board response for Codex's explicit inline display path.

No network, credentials, backend writes, analysis, or new financial calculations.
The input is a result already retrieved through the installed connector.
"""
from __future__ import annotations

import argparse
from datetime import date, datetime
import hashlib
import json
import math
from pathlib import Path
import re


def unique_object(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError("duplicate JSON field")
        out[key] = value
    return out


def reject_constant(value):
    raise ValueError("non-finite JSON number")


def render(raw: bytes, read_at: str) -> str:
    if len(raw) > 1_000_000:
        raise ValueError("board input exceeds 1 MB")
    observed = datetime.fromisoformat(read_at.replace("Z", "+00:00"))
    if observed.tzinfo is None:
        raise ValueError("read-at requires an explicit timezone")
    value = json.loads(raw, object_pairs_hook=unique_object, parse_constant=reject_constant)
    if isinstance(value, dict) and "result" in value:
        value = value["result"]
    if isinstance(value, dict) and value.get("isError"):
        raise ValueError("connector returned an error")
    if isinstance(value, dict) and "structuredContent" in value:
        value = value["structuredContent"]
    if not isinstance(value, dict) or not isinstance(value.get("rows"), list):
        raise ValueError("expected a structured board response")
    for field in ("night", "board_as_of"):
        if not isinstance(value.get(field), str) or date.fromisoformat(value[field]).isoformat() != value[field]:
            raise ValueError("board publication dates are missing or invalid")
    counts = value.get("counts")
    if not isinstance(counts, dict) or any(type(counts.get(key)) is not int or counts[key] < 0
            for key in ("top_picks", "qualified_picks", "earlier_cases")):
        raise ValueError("board counts are missing or invalid")
    if len(value["rows"]) > 500:
        raise ValueError("board exceeds the bounded display size")
    tickers = set()
    for row in value["rows"]:
        if not isinstance(row, dict) or row.get("where") != "board":
            raise ValueError("request board(set=board); mixed/library results need their own view")
        ticker = row.get("ticker")
        if not isinstance(ticker, str) or not re.fullmatch(r"[A-Z0-9.^-]{1,15}", ticker) or ticker in tickers:
            raise ValueError("missing, invalid or ambiguous ticker")
        tickers.add(ticker)
        for field in ("locked_close", "estimated_value", "gap_to_value"):
            number = row.get(field)
            if number is not None and (type(number) not in (int, float) or not math.isfinite(number)):
                raise ValueError("invalid financial number")
    payload = json.dumps({"board": value, "read_at": read_at}, ensure_ascii=True, allow_nan=False,
                         separators=(",", ":"))
    # JSON remains data even if a retained text field contains HTML/script delimiters.
    payload = payload.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    root = "sift-board-" + hashlib.sha256(payload.encode()).hexdigest()[:16]
    template = Path(__file__).resolve().parents[1] / "assets" / "board-view.html"
    fragment = template.read_text().replace("__SIFT_ROOT__", root).replace("__SIFT_PAYLOAD__", payload)
    if len(fragment.encode()) > 1_000_000:
        raise ValueError("rendered board exceeds 1 MB")
    return fragment


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--read-at", required=True)
    args = parser.parse_args()
    raw = args.input.read_bytes()
    fragment = render(raw, args.read_at)
    if args.input.resolve() == args.output.resolve():
        raise ValueError("output must not replace the input")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(fragment)
    print(json.dumps({"status": "FRAGMENT_WRITTEN_NOT_HOST_RENDER_VERIFIED", "output": str(args.output.resolve()),
                      "input_sha256": hashlib.sha256(raw).hexdigest(),
                      "fragment_sha256": hashlib.sha256(fragment.encode()).hexdigest(),
                      "network_calls": 0, "project_model_calls": 0}))


if __name__ == "__main__":
    main()
