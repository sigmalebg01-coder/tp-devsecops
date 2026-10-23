# D - Plan de restauration (proposition soumise à validation humaine)

| Rubrique | Contenu |
|----------|---------|
| Action proposée | Rollback de la version 2.4.7 vers 2.4.6 (`APP_VERSION=2.4.6`, `SIMULATE_FAILURE=false`, recréation du conteneur `api`) |
| Risque | Perte des correctifs de 2.4.7 ; compatibilité de schéma si migration appliquée ; courte indisponibilité pendant la recréation |
| Rollback du rollback | Redéploiement de 2.4.7 (image conservée) après correction |
| Validation | `/health` = 200 ; taux 5xx < 1 % pendant 10 min ; alerte `ElevatedHTTP500` résolue ; détecteur = OK |
| Observabilité post-changement | Tableau de bord Grafana « TECHCORP - Orders API » ouvert, alerte active, journaux surveillés 30 min |
| Approbation | Décision humaine enregistrée via `python -m aiops.approve` ; aucune action autonome sur la production ni la base |
| Post-mortem | Chronologie (livraison, 1ʳᵉ erreur, alerte, décision), cause racine à prouver, actions préventives (test de charge DB en CI, canary), revue sans recherche de coupable |