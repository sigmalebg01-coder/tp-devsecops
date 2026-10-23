# A1 - Registre des risques (pipeline et service Orders API)

Gravité et probabilité : 1 (faible) à 5 (élevée) ; criticité = G × P.

| # | Risque | Constat (Dockerfile / dépendances / env / workflow) | G | P | Crit. | Mesure corrective |
|---|--------|------------------------------------------------------|---|---|-------|-------------------|
| 1 | Secret committé dans le dépôt | Aucun contrôle avant ce TP ; variables d'environnement facilement copiées dans le code | 5 | 3 | 15 | Gitleaks bloquant en CI + secret scanning GitHub ; secrets uniquement dans GitHub Secrets / coffre |
| 2 | Dépendances vulnérables | `requirements.txt` en plages de versions, pas de lockfile | 4 | 4 | 16 | Trivy (HIGH/CRITICAL) bloquant ; lockfile + Dependabot ; épingler les versions en production |
| 3 | Image Docker vulnérable ou trop privilégiée | Image de base mise à jour irrégulièrement ; exécution en root si non corrigée | 4 | 3 | 12 | Utilisateur non-root (fait), scan Trivy de l'image, image de base épinglée par digest |
| 4 | Permissions excessives du workflow | `GITHUB_TOKEN` en lecture/écriture par défaut sur certains dépôts | 4 | 3 | 12 | `permissions: contents: read` au niveau du workflow (fait), droits élevés par job uniquement si nécessaire |
| 5 | Chaîne d'approvisionnement CI (actions/outils non épinglés) | Actions référencées par tag, images `latest` | 4 | 2 | 8 | Épingler les actions par SHA de commit et les images par digest ; revue des mises à jour |
| 6 | Exposition des outils d'observabilité | Grafana avec mot de passe par défaut, ports ouverts | 3 | 3 | 9 | Ports liés à 127.0.0.1 (fait), mot de passe via variable d'environnement, SSO en production |