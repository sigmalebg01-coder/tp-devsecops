# A5 - Secrets, GITHUB_TOKEN et coffres

**Secrets GitHub Actions.** Valeurs chiffrées stockées côté GitHub (dépôt, environnement ou organisation) et injectées
dans un job via `${{ secrets.NOM }}`. Elles sont masquées dans les logs, mais restent lisibles par du code malveillant
exécuté dans le job (PR depuis un fork, action compromise) : on limite donc leur portée (secrets d'environnement avec
approbation), on évite de les exposer aux PR de forks et on les fait tourner régulièrement.

**Permissions minimales du GITHUB_TOKEN.** Jeton éphémère créé pour chaque exécution. On déclare `permissions:` explicitement
(ici `contents: read`) afin que toute action compromise ne puisse ni pousser du code, ni modifier les releases, ni écrire
sur les PR. On n'élève les droits qu'au niveau du job qui en a besoin (ex. `pull-requests: write` pour commenter).

**Pourquoi un Kubernetes Secret non chiffré côté stockage n'est pas un coffre-fort complet.** Un Secret Kubernetes n'est
qu'encodé en base64 : sans chiffrement au repos d'etcd (EncryptionConfiguration / KMS), toute personne ayant accès à etcd,
à ses sauvegardes ou au droit RBAC `get secrets` lit les valeurs en clair. Un vrai coffre ajoute chiffrement et gestion
de clés, contrôle d'accès fin, audit de chaque lecture, rotation et secrets dynamiques à durée de vie courte
(Vault, cloud KMS, External Secrets Operator).