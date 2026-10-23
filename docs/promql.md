# Requêtes PromQL (B1, B2, B4)

| Usage | Requête |
|-------|---------|
| Disponibilité de la cible | `up{job="techcorp-api"}` |
| Requêtes 200 / 500 par seconde | `sum by (status) (rate(http_requests_total[1m]))` |
| Taux d'erreur 5xx (%) | `100 * (sum(rate(http_requests_total{status=~"5.."}[1m])) or vector(0)) / clamp_min(sum(rate(http_requests_total[1m])), 0.001)` |
| Débit total | `sum(rate(http_requests_total[1m]))` |
| Latence p95 | `histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket[1m])))` |
| Règle d'alerte ElevatedHTTP500 | `sum(increase(http_requests_total{status="500"}[2m])) > 5` (for: 15s) |

## B4 - Seuil d'alerte vs détection d'anomalies statistique
Un **seuil d'alerte** compare une valeur à une constante choisie à la main (> 5 erreurs en 2 min) : simple et prévisible,
mais indépendant du contexte (trafic faible ou fort, heure, saisonnalité), donc générateur de faux positifs ou de faux
négatifs. Une **détection statistique** apprend le comportement normal (baseline glissante) et mesure l'écart relatif à la
variabilité habituelle (z-score) : elle s'adapte au contexte, mais exige un historique suffisant, des hypothèses sur la
distribution et reste moins explicable. `aiops/detector.py` combine les deux : taux sur fenêtre + z-score.