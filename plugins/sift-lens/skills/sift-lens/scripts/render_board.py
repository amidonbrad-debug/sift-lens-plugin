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


def bound_method_result(board, raw, read_at):
    require(raw is not None, "EXACT_RESULT_NOT_PRELOADED")
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
    return row, result, case, cards, shared


def research_sidecar(board, raw, read_at):
    if raw is None:
        return {"status": "UNAVAILABLE", "reason": "EXACT_RESULT_NOT_PRELOADED"}
    try:
        row, result, case, cards, shared = bound_method_result(board, raw, read_at)
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


REPORT_SECTIONS = ('1 decision', '2 dashboard', '3 three assumptions', '4 what price requires',
                   '5 catalysts and breaks', 'verification', 'historical')
REPORT_REQUIREMENTS = ('source_inventory', 'quote_comparison', 'accounting_and_claims', 'drama_ledger',
                       'growth_ledger', 'quarterly_expectations', 'forecast_model', 'funding_schedule',
                       'peers_and_multiple_selection', 'valuation_policy', 'prior_run_reconciliation',
                       'pre_delivery_verification')


def report_sidecar(board, raw, read_at):
    """Read a separately bound saved report; numerical validity is independent."""
    try:
        row, result, case, cards, shared = bound_method_result(board, raw, read_at)
        run = result['by_card'][row['card_id']]
        saved = shared.get('saved_report')
        report = run.get('saved_report')
        selected_shared = saved.get('reports', {}).get(row['card_id']) if isinstance(saved, dict) and isinstance(saved.get('reports'), dict) else None
        require(report is not None or selected_shared is not None or saved is not None and not isinstance(saved, dict), 'REPORT_NOT_SUPPLIED')
        def keys(value, expected):
            return isinstance(value, dict) and set(value) == set(expected.split())
        def strings(value):
            return isinstance(value, list) and all(isinstance(v, str) and v.strip() for v in value)
        def timestamp(value):
            require(isinstance(value, str) and re.search(r'T.*(?:Z|[+-][0-9]{2}:[0-9]{2})$', value), 'REPORT_DATE_INVALID')
            parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
            require(parsed.tzinfo is not None, 'REPORT_DATE_INVALID')
            return parsed
        require(keys(saved, 'status input_sha256 input_json reports financial_acceptance')
                and isinstance(saved['reports'], dict) and isinstance(report, dict)
                and report == saved['reports'].get(row['card_id']), 'REPORT_COPIES_MISMATCH')
        require(keys(report, 'binding analyst conclusion claimed_conclusion effective_conclusion sections requirements sources limitations missing section_coverage upstream_refusals financial_acceptance methodology_complete publication_eligible identity_authentication'), 'REPORT_SHAPE_INVALID')
        require(saved['status'] == 'SAVED_REPORT_NOT_FINANCIALLY_ACCEPTED'
                and saved['financial_acceptance'] == report['financial_acceptance'] == 'NOT_PERFORMED'
                and report['methodology_complete'] is False and report['publication_eligible'] is False
                and report['effective_conclusion'] == 'WITHHELD_PENDING_INDEPENDENT_FINANCIAL_ACCEPTANCE'
                and report['identity_authentication'] == 'CALLER_DECLARED_DIGESTS_REQUIRE_INDEPENDENT_AUTHENTICATION', 'REPORT_ACCEPTANCE_OR_COMPLETENESS_INVALID')
        require(isinstance(saved['input_json'], str) and digest(saved['input_sha256'])
                and hashlib.sha256(saved['input_json'].encode()).hexdigest() == saved['input_sha256'], 'REPORT_INPUT_BYTE_HASH_MISMATCH')
        inp = strict_json(saved['input_json'])
        require(keys(inp, 'schema reports') and inp['schema'] == 'ai-trading-pilot/saved-methodology-report/v1'
                and isinstance(inp['reports'], list), 'REPORT_INPUT_SCHEMA_INVALID')
        originals = [v for v in inp['reports'] if isinstance(v, dict) and v.get('binding', {}).get('card_id') == row['card_id']]
        require(len(originals) == 1, 'REPORT_INPUT_SELECTION_AMBIGUOUS')
        original = originals[0]
        require(keys(original, 'binding analyst conclusion limitations requirements sections sources'), 'REPORT_INPUT_SHAPE_INVALID')
        binding = report['binding']
        require(keys(binding, 'case cutoff card_id manifest_sha256 facts_sha256 expected_sha256 package_sha256 card_sha256 text_sha256 source_result_sha256 forecast_input_sha256 valuation_input_sha256')
                and binding == original['binding'], 'REPORT_INPUT_BINDING_MISMATCH')
        expected = {'case': row['ticker'], 'cutoff': row['cutoff'], 'card_id': row['card_id'],
                    'card_sha256': row['card_sha256'], 'text_sha256': cards[0].get('text_sha256'),
                    'package_sha256': result.get('engine', {}).get('package_sha256'),
                    **{k: case.get(k) for k in ('manifest_sha256', 'facts_sha256', 'expected_sha256')}}
        require(all(isinstance(v, str) and v and binding[k] == v and (not k.endswith('sha256') or digest(v))
                    for k, v in expected.items()) and digest(binding['source_result_sha256']), 'REPORT_SOURCE_BINDING_MISMATCH')
        # Pre-report semantic source is bound only to the exact saved input, never
        # substituted with outer result_sha256 or case.original_result_sha256.
        for field, name in [('forecast_input_sha256', 'saved_forecast'), ('valuation_input_sha256', 'saved_valuation')]:
            numerical = shared.get(name)
            require(binding[field] is None if numerical is None else isinstance(numerical, dict)
                    and digest(numerical.get('input_sha256')) and binding[field] == numerical['input_sha256'], 'REPORT_NUMERICAL_REFERENCE_MISMATCH')
        analyst = report['analyst']
        require(keys(analyst, 'name kind authored_at assembled_at source_completed_at temporal_mode evidence note')
                and analyst == original['analyst'] and isinstance(analyst['name'], str) and analyst['name'].strip()
                and isinstance(analyst['note'], str) and analyst['note'].strip() and analyst['kind'] in ('NAMED_HUMAN_ANALYST', 'PINNED_MODEL_ANALYST', 'SYNTHETIC_TEST_FIXTURE')
                and analyst['temporal_mode'] in ('CONTEMPORANEOUS', 'RETROSPECTIVE_CUTOFF_RESTRICTED'), 'REPORT_ANALYST_MISMATCH')
        authored, assembled, cutoff = timestamp(analyst['authored_at']), timestamp(analyst['assembled_at']), timestamp(binding['cutoff'])
        require(assembled >= authored and (analyst['kind'] != 'PINNED_MODEL_ANALYST' or analyst['source_completed_at'] is not None)
                and (analyst['source_completed_at'] is None or timestamp(analyst['source_completed_at']) == authored)
                and analyst['temporal_mode'] == ('CONTEMPORANEOUS' if authored <= cutoff else 'RETROSPECTIVE_CUTOFF_RESTRICTED'), 'REPORT_AUTHORING_CLOCK_MISMATCH')
        require(keys(analyst['evidence'], 'identity_sha256 call_receipt_sha256 raw_output_sha256')
                and all(digest(v) for v in analyst['evidence'].values()), 'REPORT_DECLARED_EVIDENCE_INVALID')
        require(original['conclusion'] in ('BUY', 'WAIT', 'AVOID', 'UNAVAILABLE')
                and report['conclusion'] == report['claimed_conclusion'] == original['conclusion']
                and strings(report['limitations']) and report['limitations'] and report['limitations'] == original['limitations'], 'REPORT_CLAIM_OR_LIMITATIONS_MISMATCH')
        require(isinstance(original['sections'], list) and all(keys(v, 'section status text source_fact_ids') for v in original['sections'])
                and len({v['section'] for v in original['sections']}) == len(original['sections'])
                and all(v['section'] in REPORT_SECTIONS for v in original['sections'])
                and isinstance(report['sections'], list) and len(report['sections']) == 7
                and isinstance(run.get('report'), list) and isinstance(run.get('refusals'), list)
                and report['upstream_refusals'] == run['refusals'], 'REPORT_SECTIONS_OR_REFUSALS_INVALID')
        missing = []
        for position, name in enumerate(REPORT_SECTIONS, 1):
            section = report['sections'][position-1]
            require(keys(section, 'section status text source_fact_ids position applicability policy gate_status upstream item_ids')
                    and section['section'] == name and type(section['position']) is int and section['position'] == position
                    and section['status'] in ('SUPPLIED', 'PARTIAL', 'UNAVAILABLE') and isinstance(section['text'], str) and section['text'].strip()
                    and strings(section['source_fact_ids']) and len(set(section['source_fact_ids'])) == len(section['source_fact_ids']), 'REPORT_SECTION_INVALID')
            source = next((v for v in original['sections'] if v['section'] == name), None)
            require(all(section[k] == source[k] for k in ('status', 'text', 'source_fact_ids')) if source else
                    section['status'] == 'UNAVAILABLE' and section['text'] == 'No saved analyst section supplied.' and section['source_fact_ids'] == [], 'REPORT_SECTION_INPUT_MISMATCH')
            if source:
                require(bool(section['source_fact_ids']), 'REPORT_SECTION_SOURCE_MISSING')
            gates = [g for g in run['report'] if g.get('section') == name]
            require(len(gates) <= 1, 'REPORT_ORIGINAL_GATE_AMBIGUOUS')
            if gates:
                gate = gates[0]
                require(section['applicability'] == ('APPLICABLE_AS_REGISTERED' if gate.get('item_ids') else 'NOT_IN_CARD') and section['policy'] == gate.get('policy')
                        and section['gate_status'] == gate.get('code') and section['upstream'] == gate.get('upstream', [])
                        and section['item_ids'] == gate.get('item_ids', []), 'REPORT_ORIGINAL_GATE_MISMATCH')
            else:
                require(section['applicability'] == 'NOT_IN_CARD' and section['policy'] is None
                        and section['gate_status'] == 'NOT_IN_CARD' and section['upstream'] == [] and section['item_ids'] == [], 'REPORT_APPLICABILITY_MISMATCH')
            if gates and gates[0].get('item_ids') and section['status'] != 'SUPPLIED': missing.append('section:'+name)
        requirements = list(REPORT_REQUIREMENTS)
        if row['method_id'] == 'EGF_V1_4' and case.get('case_profile', {}).get('value') != 'ESTABLISHED':
            requirements += ['ramp_ledger', 'milestone_execution', 'unit_economics_and_breakeven', 'delay_stress']
        require(isinstance(report['requirements'], dict) and report['requirements'] == original['requirements']
                and set(report['requirements']).issubset(requirements), 'REPORT_REQUIREMENTS_MISMATCH')
        for value in report['requirements'].values():
            require(keys(value, 'status evidence_sha256 note') and value['status'] in ('SUPPLIED', 'PARTIAL', 'UNAVAILABLE')
                    and isinstance(value['note'], str) and value['note'].strip() and (value['evidence_sha256'] is None or digest(value['evidence_sha256']))
                    and (value['status'] != 'SUPPLIED' or digest(value['evidence_sha256'])), 'REPORT_REQUIREMENT_INVALID')
        missing += ['requirement:'+name for name in requirements if report['requirements'].get(name, {}).get('status') != 'SUPPLIED']
        require(report['missing'] == missing and report['section_coverage'] == ('INCOMPLETE' if missing else 'ALL_SUPPLIED_NOT_VERIFIED'), 'REPORT_MISSING_COVERAGE_MISMATCH')
        require(isinstance(original['sources'], list) and original['sources'] and all(keys(v, 'fact_id fact_sha256') for v in original['sources'])
                and len({v['fact_id'] for v in original['sources']}) == len(original['sources'])
                and isinstance(report['sources'], dict) and set(report['sources']) == {v['fact_id'] for v in original['sources']}
                and isinstance(shared.get('facts'), list), 'REPORT_SOURCES_INVALID')
        dates = []
        for source in original['sources']:
            identity = source['fact_id'];record = report['sources'][identity]
            facts = [fact for fact in shared['facts'] if fact.get('id') == identity]
            require(keys(record, 'fact_id fact_sha256 limitations') and record['fact_id'] == identity
                    and digest(source['fact_sha256']) and record['fact_sha256'] == source['fact_sha256']
                    and len(facts) == 1, 'REPORT_SOURCE_IDENTITY_MISMATCH')
            fact = facts[0]
            require(hashlib.sha256(json.dumps(fact, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest() == source['fact_sha256'], 'REPORT_SOURCE_FACT_HASH_MISMATCH')
            limits = {k: fact[k] for k in ('flags', 'conflict', 'conflicts_with', 'superseded_by', 'duplicate_of', 'value_state', 'note') if k in fact}
            require(isinstance(record['limitations'], dict), 'REPORT_SOURCE_LIMITATIONS_MISMATCH')
            for key in ('authority', 'derivation', 'source_role', 'label'):
                if key in record['limitations']:
                    require(key in fact, 'REPORT_SOURCE_LIMITATIONS_MISMATCH')
                    limits[key] = fact[key]
            require(record['limitations'] == limits, 'REPORT_SOURCE_LIMITATIONS_MISMATCH')
            dates.append({'id': identity, **{k: fact.get(k) for k in ('available_at', 'observed_at', 'period')}})
        require(all(identity in report['sources'] for section in report['sections'] for identity in section['source_fact_ids']), 'REPORT_SECTION_SOURCE_MISSING')
        return {'status': 'BOUND_REPORT', 'result_id': row['result_id'], 'read_at': read_at, 'raw_sha256': row['raw_sha256'],
                'input_sha256': saved['input_sha256'], 'report': report, 'source_dates': dates,
                'original_report': run['report'], 'original_stages': run.get('stages', [])}
    except (ValueError, TypeError, KeyError, AttributeError, IndexError) as exc:
        return {'status': 'UNAVAILABLE', 'reason': str(exc) if re.fullmatch(r'[A-Z_]+', str(exc)) else 'REPORT_MALFORMED'}


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
                          "research": research_sidecar(value, method_result, method_result_read_at),
                          "report": report_sidecar(value, method_result, method_result_read_at)}, ensure_ascii=True, allow_nan=False,
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
