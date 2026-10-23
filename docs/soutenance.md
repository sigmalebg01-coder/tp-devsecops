# D - Trame de soutenance (5 min + 3 min de questions)

1. **Pipeline rouge puis vert** (1 min) : PR `test/secret-leak` bloquée par Gitleaks, puis PR corrigée verte (captures horodatées dans `evidence/`).
2. **Grafana avant / pendant l'incident** (1 min) : tableau de bord `TECHCORP - Orders API` (cible, taux d'erreur, débit, latence).
3. **Détecteur** (1 min) : `python -m aiops.detector` ; expliquer taux sur fenêtre, baseline glissante, z-score et seuils.
4. **Rapport IA** (1 min 30) : `incident-report.md` ; **contester une hypothèse** : « la version 2.4.7 cause la panne » repose sur une
   simple corrélation temporelle, sans métrique côté base ni diff de configuration : elle reste une hypothèse.
5. **Plan de restauration** (30 s) : voir `docs/plan-restauration.md`.

Questions probables : seuil vs détection statistique ; pourquoi ne pas laisser le LLM agir ; pourquoi les logs sont non fiables ;
exception Trivy approuvée ; GITHUB_TOKEN minimal.