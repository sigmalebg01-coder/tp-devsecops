"""Orders API - service de laboratoire TECHCORP (FastAPI + metriques Prometheus)."""
import json
import os
import random
import time
from datetime import datetime, timezone

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

VERSION = os.getenv("APP_VERSION", "2.4.6")

app = FastAPI(title="Orders API", version=VERSION)

REQUESTS = Counter("http_requests_total", "Total des requetes HTTP", ["method", "route", "status"])
LATENCY = Histogram(
    "http_request_duration_seconds",
    "Latence des requetes HTTP",
    ["route"],
    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5),
)


def failure_enabled() -> bool:
    """Lu a chaque requete pour pouvoir etre modifie dans les tests."""
    return os.getenv("SIMULATE_FAILURE", "false").lower() == "true"


def log(level: str, msg: str, **fields) -> None:
    """Une ligne JSON par evenement, sur la sortie standard (docker logs)."""
    record = {"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
              "level": level, "msg": msg, "version": VERSION}
    record.update(fields)
    print(json.dumps(record), flush=True)


@app.middleware("http")
async def instrument(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    route = request.scope.get("route")
    path = route.path if route is not None else "unmatched"
    if path != "/metrics":
        REQUESTS.labels(request.method, path, str(response.status_code)).inc()
        LATENCY.labels(path).observe(time.perf_counter() - start)
    return response


@app.get("/health")
def health():
    return {"status": "ok", "version": VERSION}


@app.get("/orders")
def orders():
    if failure_enabled():
        time.sleep(random.uniform(0.3, 0.8))
        log("ERROR", "db_connection_timeout", route="/orders", status=500)
        return JSONResponse(status_code=500, content={"error": "db_connection_timeout"})
    time.sleep(random.uniform(0.02, 0.12))
    log("INFO", "orders_listed", route="/orders", status=200)
    return {"orders": [{"id": 1, "total": 42.5}, {"id": 2, "total": 19.9}]}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)