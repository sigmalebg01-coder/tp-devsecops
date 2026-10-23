# TECHCORP - Orders API : DevSecOps & AIOps (TP intégrateur)

Service de laboratoire FastAPI (`/orders`, `/health`, `/metrics`) avec pipeline de confiance (Pytest, Gitleaks, Trivy),
observabilité (Prometheus, Grafana) et investigation AIOps (détecteur Python + Ollama, rapport soumis à validation humaine).

## Prérequis
Docker Desktop, Git, Python 3.11+, (Ollama facultatif : repli en mode simulé documenté dans le rapport).

## Reproduction
```powershell
docker compose up --build -d          # API :8000, Prometheus :9090, Grafana :3000 (admin / techcorp-lab)
python -m venv .venv ; .\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m pytest -q   # tests API, détecteur, masquage

# Incident de laboratoire (local uniquement)
$env:APP_VERSION='2.4.7'; $env:SIMULATE_FAILURE='true'; docker compose up -d --force-recreate api
1..20 | ForEach-Object { try { Invoke-WebRequest http://localhost:8000/orders -UseBasicParsing } catch {} }

# Détection, rapport IA, approbation humaine
.\.venv\Scripts\python -m aiops.detector --out evidence/detector.json
.\.venv\Scripts\python -m aiops.incident_report            # ajouter --mock pour le mode simulé
.\.venv\Scripts\python -m aiops.approve --decision approved --by "Prenom Nom"
```

## Contenu
| Chemin | Rôle |
|--------|------|
| `app/` | API FastAPI instrumentée (métriques, logs JSON) |
| `.github/workflows/ci.yml` | Pytest + Gitleaks + Trivy (fs et image), `permissions: contents: read` |
| `docs/risk-register.md`, `docs/quality-gate.md`, `docs/security-notes.md` | A1, A3, A5 |
| `prometheus/`, `grafana/` | Cible `techcorp-api`, règle `ElevatedHTTP500`, tableau de bord provisionné |
| `docs/promql.md` | Requêtes PromQL et B4 |
| `aiops/` | Détecteur (fenêtre + z-score), masquage, rapport LLM, approbation |
| `report.json`, `incident-report.md` | Rapport d'incident généré |
| `docs/plan-restauration.md`, `docs/soutenance.md` | Mission D |