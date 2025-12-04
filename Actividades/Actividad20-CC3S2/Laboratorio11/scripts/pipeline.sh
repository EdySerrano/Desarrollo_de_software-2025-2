#!/usr/bin/env bash
set -euo pipefail
SERVICE="${SERVICE:-order-service}"
SCAN_FAIL_SEVERITY="${SCAN_FAIL_SEVERITY:-high}"
COSIGN_VERIFY="${COSIGN_VERIFY:-0}"

echo "=================================================="
echo "Iniciando Pipeline Local para: $SERVICE"
echo "Severity Gate: $SCAN_FAIL_SEVERITY | Cosign Verify: $COSIGN_VERIFY"
echo "=================================================="

# Ejecuta el pipeline completo (CI local)
# Esto invoca: env -> minikube-up -> build -> push (skip) -> sbom -> sign -> scan -> k8s-prepare -> k8s-apply -> smoke
make pipeline SERVICE="$SERVICE" SCAN_FAIL_SEVERITY="$SCAN_FAIL_SEVERITY" COSIGN_VERIFY="$COSIGN_VERIFY"

echo "=================================================="
echo "Pipeline Finalizado Exitosamente para: $SERVICE"
echo "=================================================="
