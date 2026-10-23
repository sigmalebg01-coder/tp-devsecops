"""Detecteur d'anomalies HTTP 5xx : fenetre temporelle + baseline glissante (z-score).

Le coeur (`evaluate`) est une fonction pure, testable sans Prometheus.
Usage : python -m aiops.detector --prometheus http://localhost:9090
Code de sortie : 0 = OK / DEGRADED / INSUFFICIENT_DATA, 2 = ANOMALY.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
import urllib.parse
import urllib.request


def error_ratio(errors, totals) -> float:
    total = sum(totals)
    return min(sum(errors) / total, 1.0) if total > 0 else 0.0


def zscore(value: float, history, min_std: float = 0.02):
    """z-score de `value` par rapport a l'historique ; None si historique trop court.

    L'ecart-type est plafonne par le bas (min_std) : une baseline parfaitement plate
    ne doit pas rendre le moindre ecart 'infiniment' anormal.
    """
    if len(history) < 3:
        return None
    mean = statistics.fmean(history)
    std = max(statistics.pstdev(history), min_std)
    return (value - mean) / std


def evaluate(errors, totals, window: int = 4, ratio_threshold: float = 0.20,
             z_threshold: float = 3.0, min_requests: float = 5) -> dict:
    """errors/totals : requetes par pas de temps (ordre chronologique)."""
    n = min(len(errors), len(totals))
    errors, totals = list(errors[:n]), list(totals[:n])
    win_err, win_tot = errors[-window:], totals[-window:]
    base_err, base_tot = errors[:-window], totals[:-window]

    ratio = error_ratio(win_err, win_tot)
    baseline = [min(e / t, 1.0) for e, t in zip(base_err, base_tot) if t > 0]
    z = zscore(ratio, baseline)
    requests_in_window = sum(win_tot)

    reasons = [f"fenetre = {len(win_tot)} derniers pas ; {requests_in_window:.0f} requetes, "
               f"{sum(win_err):.0f} erreurs 5xx ; taux = {ratio:.1%}"]
    if requests_in_window < min_requests:
        verdict = "INSUFFICIENT_DATA"
        reasons.append(f"moins de {min_requests:.0f} requetes dans la fenetre : conclusion impossible")
    elif ratio >= ratio_threshold:
        if z is None:
            verdict = "ANOMALY"
            reasons.append(f"taux >= seuil fixe {ratio_threshold:.0%} ; baseline insuffisante pour le z-score")
        elif z >= z_threshold:
            verdict = "ANOMALY"
            reasons.append(f"taux >= seuil {ratio_threshold:.0%} ET z-score {z:.1f} >= {z_threshold}")
        else:
            verdict = "DEGRADED"
            reasons.append(f"taux >= seuil mais z-score {z:.1f} < {z_threshold} : dans la variabilite habituelle")
    elif ratio >= ratio_threshold / 2:
        verdict = "DEGRADED"
        reasons.append(f"taux >= {ratio_threshold / 2:.0%} (moitie du seuil)")
    else:
        verdict = "OK"
        reasons.append("taux sous les seuils")

    return {
        "verdict": verdict,
        "error_ratio": round(ratio, 4),
        "window_requests": round(requests_in_window, 2),
        "window_errors": round(sum(win_err), 2),
        "baseline_points": len(baseline),
        "baseline_mean": round(statistics.fmean(baseline), 4) if baseline else None,
        "zscore": None if z is None else round(z, 2),
        "thresholds": {"ratio": ratio_threshold, "zscore": z_threshold,
                       "min_requests": min_requests, "window_steps": window},
        "reasons": reasons,
    }


# ---------------------------------------------------------------- Prometheus
def _query_range(base: str, expr: str, start: float, end: float, step: int) -> dict:
    qs = urllib.parse.urlencode({"query": expr, "start": start, "end": end, "step": step})
    with urllib.request.urlopen(f"{base}/api/v1/query_range?{qs}", timeout=10) as resp:
        data = json.load(resp)
    result = data["data"]["result"]
    return {float(ts): float(val) for ts, val in (result[0]["values"] if result else [])}


def fetch_series(base: str, lookback_s: int = 1800, step: int = 30):
    end = time.time()
    start = end - lookback_s
    totals = _query_range(base, f'sum(increase(http_requests_total[{step}s]))', start, end, step)
    errors = _query_range(base, f'sum(increase(http_requests_total{{status=~"5.."}}[{step}s]))',
                          start, end, step)
    timeline = sorted(totals)
    return ([errors.get(ts, 0.0) for ts in timeline], [totals[ts] for ts in timeline], timeline)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--prometheus", default="http://localhost:9090")
    ap.add_argument("--lookback", type=int, default=1800, help="secondes d'historique")
    ap.add_argument("--step", type=int, default=30, help="pas en secondes")
    ap.add_argument("--window", type=int, default=4, help="nombre de pas dans la fenetre")
    ap.add_argument("--ratio-threshold", type=float, default=0.20)
    ap.add_argument("--z-threshold", type=float, default=3.0)
    ap.add_argument("--out", help="fichier JSON de sortie")
    args = ap.parse_args(argv)

    errors, totals, timeline = fetch_series(args.prometheus, args.lookback, args.step)
    result = evaluate(errors, totals, args.window, args.ratio_threshold, args.z_threshold)
    result["evaluated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    result["points"] = len(timeline)
    text = json.dumps(result, indent=2, ensure_ascii=False)
    print(text)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
    return 2 if result["verdict"] == "ANOMALY" else 0


if __name__ == "__main__":
    sys.exit(main())