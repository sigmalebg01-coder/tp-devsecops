# A3 - Quality gate de la pull request

Une PR ne peut être fusionnée que si **tous** les jobs requis (`tests`, `secret-scan`, `trivy`) sont verts
(règle de protection de branche `main` : « Require status checks to pass »).

| Résultat | Décision | Justification |
|----------|----------|---------------|
| Secret détecté par Gitleaks (tout niveau) | **Bloque** | Un secret exposé est compromis dès le commit ; réécrire l'historique et révoquer |
| Vulnérabilité **CRITICAL/HIGH avec correctif disponible** (dépendance ou image) | **Bloque** | Exploitable et corrigeable : mettre à jour |
| Vulnérabilité HIGH/CRITICAL **sans correctif** (`--ignore-unfixed`) | Ne bloque pas, suivie | Rien à appliquer ; reste visible au rapport et revue périodique |
| MEDIUM / LOW | Ne bloque pas, rapportée | Traitées au fil de l'eau (backlog) |
| Tests Pytest en échec | **Bloque** | Régression fonctionnelle |

## Vulnérabilité exploitable, faux positif, exception approuvée
- **Exploitable** : le composant est présent *et* le code vulnérable est atteignable dans notre usage → on corrige.
- **Faux positif** : le composant ou la fonction vulnérable n'est pas utilisé (preuve écrite) → entrée `.trivyignore`.
- **Exception approuvée** : risque accepté temporairement ; entrée `.trivyignore` avec identifiant, justification,
  approbateur et **date d'expiration**, validée par un second relecteur (CODEOWNERS Sécurité).