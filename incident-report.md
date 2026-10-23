# Rapport d'incident - Orders API 2.4.7

- Genere le : 2026-10-23T15:58:06Z
- Mode d'analyse : **simulated**
- Verdict du detecteur : **OK** (taux 5xx 0.0%, z-score 0.0)
- Statut de la remediation : **PENDING_HUMAN_APPROVAL**

## Contexte du changement
```json
{
  "version": "2.4.7",
  "previous_version": "2.4.6",
  "deployed_at": null,
  "note": "evidence/change.json absent : heure du changement inconnue"
}
```

## Symptomes
- Taux d'erreurs 5xx de 0.0% sur la fenetre, verdict OK
- Statuts dans les logs : {'200': 7}

## Hypotheses (non prouvees)
| Hypothese | Confiance | Preuves |
|---|---|---|
| La version 2.4.7 introduit une regression de connexion a la base (correlation temporelle uniquement) | medium | 1re erreur None ; changement None ; versions vues : ['2.4.6'] |
| La base de donnees est saturee ou indisponible independamment de la livraison | low | Aucune metrique cote base disponible pour trancher |
| Probleme reseau/DNS entre l'API et la base | low | Message db_connection_timeout compatible, non verifie |

## Preuves collectees
- db_connection_timeout vu a None
- z-score = 0.0, baseline = 57 points

## Controles non destructifs proposes
- Comparer la configuration (pool, timeouts) entre les versions precedente et courante
- Lire en lecture seule les metriques de la base (connexions, latence)
- Verifier la resolution DNS et la joignabilite reseau depuis le conteneur API

## Limites
- Mode SIMULE : aucune analyse LLM reelle
- Pas de metriques cote base de donnees
- Correlation temporelle != causalite

## Remediation proposee
Rollback de 2.4.7 vers 2.4.6 (a valider par un humain, non execute)

> Toute action (redemarrage, rollback) exige une approbation humaine explicite : voir `python -m aiops.approve`.

## Resume des logs (masques, bornes)
```json
{
  "lines_analysed": 128,
  "status_counts": {
    "200": 7
  },
  "versions_seen": [
    "2.4.6"
  ],
  "error_lines": 0,
  "first_error_ts": null,
  "first_db_connection_timeout_ts": null
}
```

## Decision humaine
- Decision : **approved** par matheo le 2026-10-23T15:59:18Z
- Remediation concernee : Rollback de 2.4.7 vers 2.4.6 (a valider par un humain, non execute)
- Cet outil n'execute aucune action : l'operation reste a realiser par un humain.
