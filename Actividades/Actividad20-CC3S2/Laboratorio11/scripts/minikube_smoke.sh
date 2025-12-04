#!/usr/bin/env bash
set -euo pipefail

SERVICE="${1:-user-service}"
PORT="${2:-8000}"
NS="${3:-default}"

echo "[i] smoke: $SERVICE/$NS -> http://127.0.0.1:${PORT}"

# Esperar a que haya al menos un pod Running
echo "[i] Esperando pod Running para $SERVICE..."
RETRIES=30
SLEEP=2
FOUND=0
for ((i=0; i<RETRIES; i++)); do
  POD="$(kubectl -n "$NS" get pods -l app="$SERVICE" -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || true)"
  if [ -n "$POD" ]; then
    STATUS="$(kubectl -n "$NS" get pod "$POD" -o jsonpath='{.status.phase}' 2>/dev/null || true)"
    if [ "$STATUS" = "Running" ]; then
      FOUND=1
      break
    fi
  fi
  echo -n "."
  sleep $SLEEP
done
echo ""

if [ $FOUND -eq 0 ]; then
  echo "[!] No se encontró pod Running para $SERVICE tras $((RETRIES*SLEEP))s"
  exit 1
fi

echo "[i] Pod encontrado: $POD"

# Port-forward en background
kubectl -n "$NS" port-forward "pod/${POD}" "${PORT}:${PORT}" >/tmp/pf_${SERVICE}.log 2>&1 &
PF_PID=$!
# Dar tiempo al port-forward para establecerse
sleep 3

# Curl health con reintentos
echo "[i] Verificando /health..."
HEALTH_RETRIES=5
HEALTH_SLEEP=2
HEALTH_OK=0

set +e
for ((j=0; j<HEALTH_RETRIES; j++)); do
  curl -fsS "http://127.0.0.1:${PORT}/health" >/dev/null 2>&1
  RC=$?
  if [ $RC -eq 0 ]; then
    HEALTH_OK=1
    break
  fi
  echo -n "x"
  sleep $HEALTH_SLEEP
done
set -e
echo ""

kill $PF_PID >/dev/null 2>&1 || true
wait $PF_PID 2>/dev/null || true

if [ $HEALTH_OK -eq 1 ]; then
  echo "[OK] SMOKE $SERVICE -> 200"
else
  echo "[!] SMOKE $SERVICE FALLÓ (RC=$RC)"
  cat /tmp/pf_${SERVICE}.log || true
  exit 1
fi
