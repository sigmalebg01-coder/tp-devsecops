from aiops.detector import error_ratio, evaluate, zscore


def healthy(n, per_step=10):
    return [0.0] * n, [float(per_step)] * n


def test_error_ratio_basic_and_empty():
    assert error_ratio([1, 1], [5, 5]) == 0.2
    assert error_ratio([0, 0], [0, 0]) == 0.0


def test_ok_when_no_errors():
    errors, totals = healthy(10)
    assert evaluate(errors, totals)["verdict"] == "OK"


def test_anomaly_when_errors_spike_over_healthy_baseline():
    errors, totals = healthy(8)
    errors += [10.0, 10.0, 10.0, 10.0]
    totals += [10.0, 10.0, 10.0, 10.0]
    result = evaluate(errors, totals)
    assert result["verdict"] == "ANOMALY"
    assert result["zscore"] >= 3.0
    assert any("z-score" in r for r in result["reasons"])


def test_insufficient_data_with_too_few_requests():
    assert evaluate([1.0, 0.0], [2.0, 1.0])["verdict"] == "INSUFFICIENT_DATA"


def test_window_is_respected():
    # des erreurs anciennes, hors fenetre, ne doivent pas declencher l'alerte
    errors = [10.0] * 3 + [0.0] * 8
    totals = [10.0] * 11
    assert evaluate(errors, totals, window=4)["verdict"] == "OK"


def test_noisy_baseline_gives_degraded_not_anomaly():
    # baseline deja tres bruitee : un taux eleve reste dans la variabilite habituelle
    errors = [6.0, 0.0, 7.0, 0.0, 6.0, 1.0, 6.0, 7.0, 6.0, 7.0]
    totals = [10.0] * 10
    result = evaluate(errors, totals, window=2, ratio_threshold=0.2, z_threshold=3.0)
    assert result["verdict"] == "DEGRADED"


def test_zscore_needs_history():
    assert zscore(0.5, [0.0, 0.0]) is None
    assert zscore(0.5, [0.0, 0.0, 0.0]) > 3