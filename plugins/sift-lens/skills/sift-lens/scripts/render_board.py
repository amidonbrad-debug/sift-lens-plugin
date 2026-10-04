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


def strict_json(raw):
    return json.loads(raw, object_pairs_hook=unique_object, parse_constant=reject_constant)


def unwrap(value):
    if isinstance(value, dict) and "result" in value:
        value = value["result"]
    if isinstance(value, dict) and value.get("isError"):
        raise ValueError("connector returned an error")
    if isinstance(value, dict) and "structuredContent" in value:
        value = value["structuredContent"]
    return value


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def digest(value):
    return isinstance(value, str) and re.fullmatch(r"[a-f0-9]{64}", value) is not None


def decimal_source(value):
    # Source decimals remain strings. No float conversion, rounding or new valuation.
    valid = isinstance(value, str) and len(value) <= 160 and re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?", value)
    return {"value": value if valid else None,
            "reason": None if valid else "NOT_SUPPLIED" if value is None else "MALFORMED_DECIMAL"}


def research_sidecar(board, raw, read_at):
    if raw is None:
        return {"status": "UNAVAILABLE", "reason": "EXACT_RESULT_NOT_PRELOADED"}
    try:
        require(len(raw) <= 1_000_000, "METHOD_RESULT_EXCEEDS_BOUND")
        require(isinstance(read_at, str) and datetime.fromisoformat(read_at.replace("Z", "+00:00")).tzinfo is not None,
                "METHOD_RESULT_READ_TIME_INVALID")
        response = unwrap(strict_json(raw))
        require(isinstance(response, dict) and isinstance(board.get("method_id"), str), "METHOD_BOARD_REQUIRED")
        require(response.get("status") != "UNAVAILABLE", "EXACT_RESULT_UNAVAILABLE")
        metadata = board.get("methodology", {})
        other = response.get("methodology", {})
        require(metadata.get("status") == other.get("status") == "AVAILABLE"
                and metadata.get("schema") == other.get("schema") == "sift-methodology-consumer/v1"
                and digest(metadata.get("revision")) and metadata.get("revision") == other.get("revision"),
                "METHOD_REVISION_MISMATCH")
        snapshot = metadata.get("snapshot", {})
        fields = ("release_id", "accepted_night", "original_candidate_sha256", "company_index_revision")
        require(all(isinstance(snapshot.get(k), str) and snapshot[k]
                    and snapshot[k] == other.get("snapshot", {}).get(k) for k in fields)
                and snapshot["accepted_night"] == board.get("night"), "SNAPSHOT_MISMATCH")
        row = response.get("method_result", {})
        matches = [item for item in board.get("records", []) if item.get("result_id") == row.get("result_id")]
        require(len(matches) == 1, "SELECTED_RESULT_NOT_ON_BOARD")
        selected = matches[0]
        # Bind every summary field, including review/selection. Overlap is independent.
        require({k: v for k, v in selected.items() if k != "qualification_overlap"} == row,
                "METHOD_SUMMARY_MISMATCH")
        require(response.get("method_id") == row.get("method_id") == board["method_id"], "METHOD_MISMATCH")
        inventory = [m for m in metadata.get("methods", []) if m.get("method_id") == row["method_id"]]
        require(len(inventory) == 1 and inventory == [m for m in other.get("methods", []) if m.get("method_id") == row["method_id"]]
                and all(row.get(k) == inventory[0].get(k) for k in ("method_version", "card_id", "card_sha256", "adoption_status")),
                "METHOD_CARD_MISMATCH")
        source = response.get("raw_json")
        require(isinstance(source, str) and digest(row.get("raw_sha256"))
                and hashlib.sha256(source.encode()).hexdigest() == row["raw_sha256"], "RAW_BYTE_HASH_MISMATCH")
        result = strict_json(source)
        require(result.get("schema") == "ai-trading-pilot/framework-case-result/v1"
                and digest(row.get("result_sha256")) and result.get("result_sha256") == row["result_sha256"]
                and row["result_id"] == f"framework-result:{row['result_sha256']}:{row['method_id']}", "RAW_RESULT_IDENTITY_MISMATCH")
        case = result.get("case", {})
        require(case.get("id") == case.get("ticker") == row.get("company_id") == row.get("ticker")
                and case.get("cutoff") == row.get("cutoff"), "RAW_COMPANY_CUTOFF_MISMATCH")
        cards = [c for c in result.get("cards", []) if c.get("card_id") == row.get("card_id")]
        require(len(cards) == 1 and cards[0].get("card_sha256") == row.get("card_sha256")
                and row.get("card_id") in result.get("by_card", {}), "RAW_CARD_MISMATCH")
        shared = result.get("shared", {})
        v, f = shared.get("saved_valuation"), shared.get("saved_forecast")
        require(isinstance(v, dict) and isinstance(f, dict), "NUMERICAL_RESEARCH_NOT_SUPPLIED")
        inputs = []
        for item, schema in ((v, "ai-trading-pilot/method-numerical-input/v1"), (f, "ai-trading-pilot/saved-analyst-forecast/v1")):
            require(isinstance(item.get("input_json"), str) and digest(item.get("input_sha256"))
                    and hashlib.sha256(item["input_json"].encode()).hexdigest() == item["input_sha256"], "INPUT_BYTE_HASH_MISMATCH")
            inp = strict_json(item["input_json"])
            require(inp.get("schema") == schema, "INPUT_SCHEMA_MISMATCH")
            inputs.append(inp)
        vi, fi = inputs
        binding = v.get("binding")
        require(isinstance(binding, dict) and binding == f.get("binding") == vi.get("binding") == fi.get("binding")
                and v.get("forecast_input_sha256") == vi.get("forecast_input_sha256") == f["input_sha256"], "NUMERICAL_CROSS_BINDING_MISMATCH")
        expected = {"case": row["ticker"], "cutoff": row["cutoff"], "card_id": row["card_id"],
                    "card_sha256": row["card_sha256"], "text_sha256": cards[0].get("text_sha256"),
                    "package_sha256": result.get("engine", {}).get("package_sha256"),
                    **{k: case.get(k) for k in ("manifest_sha256", "facts_sha256", "expected_sha256")}}
        require(all(binding.get(k) == val and isinstance(val, str) and val for k, val in expected.items())
                and all(digest(binding.get(k)) for k in (*[k for k in expected if k.endswith("sha256")], "source_result_sha256")),
                "SELECTED_NUMERICAL_BINDING_MISMATCH")
        horizons = v.get("horizons", [])
        require(isinstance(horizons, list) and len(horizons) <= 12, "HORIZONS_INVALID")
        projected = []
        def bound_currency(scenario, name, horizon):
            currency = fi.get("currency")
            require(currency == "USD", "FORECAST_CURRENCY_UNAVAILABLE")
            refs, rows = scenario.get("forecast_rows", {}), fi.get("scenarios", {}).get(name, [])
            require(isinstance(rows, list), "FORECAST_ROWS_UNAVAILABLE")
            for key, metric in (("metric_row", scenario.get("metric")), ("cash_row", "cash"), ("debt_row", "debt"), ("shares_row", "diluted_shares")):
                index = refs.get(key)
                require(type(index) is int and 0 <= index < len(rows), "FORECAST_ROW_BINDING_UNAVAILABLE")
                ref = rows[index]
                require(ref.get("metric") == metric and decimal_source(ref.get("value"))["value"] is not None,
                        "FORECAST_ROW_VALUE_INVALID")
                require(ref.get("unit") == ("SHARES" if key == "shares_row" else "CURRENCY")
                        and ref.get("currency") == ("NOT_APPLICABLE" if key == "shares_row" else currency), "FORECAST_ROW_UNITS_UNAVAILABLE")
                if key == "metric_row":
                    require(ref.get("period") == scenario.get("metric_period")
                            and ref.get("accounting_basis") == scenario.get("accounting_basis")
                            and ref.get("sbc_basis") == scenario.get("sbc_basis"), "FORECAST_FINANCIAL_BASIS_MISMATCH")
            require(scenario.get("target_date") == horizon and scenario.get("scenario") == name,
                    "SCENARIO_HORIZON_MISMATCH")
            date.fromisoformat(horizon)
            return currency
        for horizon in horizons:
            require(isinstance(horizon, dict), "HORIZON_INVALID")
            scenarios = []
            for name in ("BEAR", "BASE", "BULL"):
                scenario = horizon.get("scenarios", {}).get(name)
                if not isinstance(scenario, dict):
                    scenarios.append({"name": name, "amount": decimal_source(None), "currency": None, "reason": "SCENARIO_NOT_SUPPLIED"})
                    continue
                try:
                    currency, reason = bound_currency(scenario, name, horizon.get("date")), None
                except (ValueError, TypeError, AttributeError, KeyError):
                    currency, reason = None, "FORECAST_CURRENCY_OR_BASIS_NOT_BOUND"
                scenarios.append({"name": name, "amount": decimal_source(scenario.get("value_per_share")), "currency": currency, "reason": reason,
                    "basis": {k: scenario.get(k) for k in ("metric", "metric_value", "metric_period", "multiple", "accounting_basis", "sbc_basis", "economic_shares", "price_return")},
                    "opening_balance_source_status": scenario.get("funding", {}).get("opening_balance_source_status")})
            projected.append({"date": horizon.get("date"), "scenarios": scenarios})
        current = v.get("current_fundamental", {})
        entry = v.get("entry", {})
        def horizon_currency(reference_date):
            matching = [h for h in projected if h["date"] == reference_date]
            currencies = [s["currency"] for h in matching for s in h["scenarios"]]
            return currencies[0] if len(matching) == 1 and len(currencies) == 3 and all(c == "USD" for c in currencies) else None
        entry_currency = horizon_currency(entry.get("horizon"))
        # Reviewed current-fundamental calculation discounts this exact reference
        # horizon by a dimensionless equity rate; currency is inherited only here.
        current_currency = horizon_currency(current.get("reference_date"))
        roles = f.get("source_roles", {})
        facts = shared.get("facts", [])
        sources = [{"id": key, "role": role.get("role"), "dates": [{k: fact.get(k) for k in ("available_at", "observed_at", "period", "source", "flags")} for fact in facts if fact.get("id") == key]}
                   for key, role in roles.items()]
        return {"status": "BOUND_REFERENCE", "result_id": row["result_id"], "read_at": read_at,
                "raw_sha256": row["raw_sha256"], "input_sha256": v["input_sha256"], "forecast_input_sha256": f["input_sha256"], "binding": binding,
                "financial_acceptance": v.get("financial_acceptance"), "completeness": v.get("completeness"), "decision": v.get("decision"),
                "status_label": v.get("status"), "quote": v.get("quote"), "route": v.get("route"), "analyst": f.get("analyst"), "case_mode": case.get("mode"),
                "current": {**{k: current.get(k) for k in ("status", "as_of", "reference_date", "method", "limitation", "equity_discount_rate")},
                    "central": decimal_source(current.get("central")), "range": {k: decimal_source(current.get("range", {}).get(k)) for k in ("low", "high")}, "currency": current_currency},
                "horizons": projected,
                "entry": {**{k: entry.get(k) for k in ("status", "financial_acceptance", "horizon", "profile", "binding_constraint", "funding_supported", "opening_balances_verified", "base_hurdle", "stress_floor")},
                    "conditional": decimal_source(entry.get("conditional_maximum_entry")), "policy_qualified": decimal_source(entry.get("maximum_policy_qualified_entry")), "currency": entry_currency},
                "assumptions": {"valuation": v.get("assumptions"), "forecast": f.get("assumptions"), "current_rationale": current.get("rationale"), "entry_note": entry.get("note")}, "sources": sources}
    except (ValueError, TypeError, KeyError, AttributeError, IndexError) as exc:
        reason = str(exc) if re.fullmatch(r"[A-Z_]+", str(exc)) else "METHOD_RESULT_MALFORMED"
        return {"status": "UNAVAILABLE", "reason": reason}


def render(raw: bytes, read_at: str, method_result: bytes | None = None, method_result_read_at: str | None = None) -> str:
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
    if not isinstance(value, dict):
        raise ValueError("expected a structured board response")
    method_board = "method_id" in value
    rows = value.get("records" if method_board else "rows")
    if not isinstance(rows, list):
        raise ValueError("expected a structured board response")
    if method_board:
        method_id = value["method_id"]
        metadata = value.get("methodology")
        if (not isinstance(method_id, str) or not re.fullmatch(r"[A-Z][A-Z0-9_]{0,63}", method_id)
                or not isinstance(metadata, dict)
                or metadata.get("schema") != "sift-methodology-consumer/v1"
                or metadata.get("status") not in ("AVAILABLE", "UNAVAILABLE", "INVALID")):
            raise ValueError("method board identity or consumer status is invalid")
        if metadata["status"] != "AVAILABLE" and rows:
            raise ValueError("unavailable method board cannot carry results")
    for field in ("night", "board_as_of"):
        if not isinstance(value.get(field), str) or date.fromisoformat(value[field]).isoformat() != value[field]:
            raise ValueError("board publication dates are missing or invalid")
    counts = value.get("counts")
    if not method_board and (not isinstance(counts, dict) or any(type(counts.get(key)) is not int or counts[key] < 0
            for key in ("top_picks", "qualified_picks", "earlier_cases"))):
        raise ValueError("board counts are missing or invalid")
    if len(rows) > 500:
        raise ValueError("board exceeds the bounded display size")
    tickers = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("invalid company record")
        if not method_board and row.get("where") != "board":
            raise ValueError("request board(set=board); mixed/library results need their own view")
        ticker = row.get("ticker")
        if not isinstance(ticker, str) or not re.fullmatch(r"[A-Z0-9.^-]{1,15}", ticker) or ticker in tickers:
            raise ValueError("missing, invalid or ambiguous ticker")
        tickers.add(ticker)
        if method_board:
            if row.get("method_id") != method_id or row.get("company_id") != ticker:
                raise ValueError("method result does not match the selected method/company")
            if row.get("result_state") not in ("COMPLETE", "PARTIAL", "NOT_APPLICABLE", "REFUSED", "UNAVAILABLE"):
                raise ValueError("method result state is invalid")
        for field in ("locked_close", "estimated_value", "gap_to_value"):
            number = row.get(field)
            if number is not None and (type(number) not in (int, float) or not math.isfinite(number)):
                raise ValueError("invalid financial number")
    payload = json.dumps({"board": value, "read_at": read_at,
                          "research": research_sidecar(value, method_result, method_result_read_at)}, ensure_ascii=True, allow_nan=False,
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
    parser.add_argument("--method-result", type=Path)
    parser.add_argument("--method-result-read-at")
    args = parser.parse_args()
    if bool(args.method_result) != bool(args.method_result_read_at):
        parser.error("--method-result and --method-result-read-at must be supplied together")
    raw = args.input.read_bytes()
    detail = args.method_result.read_bytes() if args.method_result else None
    fragment = render(raw, args.read_at, detail, args.method_result_read_at)
    if args.input.resolve() == args.output.resolve() or (args.method_result and args.method_result.resolve() == args.output.resolve()):
        raise ValueError("output must not replace the input")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(fragment)
    print(json.dumps({"status": "FRAGMENT_WRITTEN_NOT_HOST_RENDER_VERIFIED", "output": str(args.output.resolve()),
                      "input_sha256": hashlib.sha256(raw).hexdigest(),
                      "method_result_sha256": hashlib.sha256(detail).hexdigest() if detail else None,
                      "fragment_sha256": hashlib.sha256(fragment.encode()).hexdigest(),
                      "network_calls": 0, "project_model_calls": 0}))


if __name__ == "__main__":
    main()
