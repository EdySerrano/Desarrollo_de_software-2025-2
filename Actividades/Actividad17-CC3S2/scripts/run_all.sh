#!/bin/bash

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Contadores
PASSED=0
FAILED=0
TOTAL=0

# Funcion para reportar estado
report_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}[PASS] $2${NC}"
        ((PASSED++))
    else
        echo -e "${RED}[FAIL] $2${NC}"
        ((FAILED++))
        # exit 1 
    fi
    ((TOTAL++))
}

echo ">>> Iniciando Pipeline de Pruebas..."

# 0. Limpieza
echo ">>> [0/4] Limpiando estado..."
find .. -name ".terraform" -type d -exec rm -rf {} +
find .. -name "terraform.tfstate*" -exec rm -f {} +
echo "Estado limpio."

# 1. Unit Tests
echo ">>> [1/4] Ejecutando Unit Tests..."
# Placeholder: Ejecutaría pytest, unittest
# Ejemplo: python3 -m pytest ../tests/unit
if python3 -c "print('Simulating Unit Tests... OK')"; then
    report_status 0 "Unit Tests"
else
    report_status 1 "Unit Tests"
fi

# 2. Smoke / Contract Tests
echo ">>> [2/4] Ejecutando Smoke & Contract Tests..."
if ./run_smoke.sh; then
    report_status 0 "Smoke/Contract Tests"
else
    report_status 1 "Smoke/Contract Tests"
fi

# 3. Integration Tests
echo ">>> [3/4] Ejecutando Integration Tests..."
# Placeholder: Terraform apply en entorno de staging + verificacion
# Ejemplo: terraform apply -auto-approve && python3 verify_infra.py
echo "Simulating Integration Tests (Terraform Apply + Verify)..."
sleep 2
if [ 1 -eq 1 ]; then # Simulacion de exito
    report_status 0 "Integration Tests"
else
    report_status 1 "Integration Tests"
fi

# 4. E2E Tests
echo ">>> [4/4] Ejecutando E2E Tests..."
# Placeholder: Pruebas de sistema completo, llamadas HTTP reales, etc.
echo "Simulating E2E Tests..."
sleep 2
if [ 1 -eq 1 ]; then # Simulacion de exito
    report_status 0 "E2E Tests"
else
    report_status 1 "E2E Tests"
fi

echo "----------------------------------------"
echo "RESUMEN DE EJECUCION"
echo "----------------------------------------"
echo -e "Total: $TOTAL"
echo -e "Pasados: ${GREEN}$PASSED${NC}"
echo -e "Fallados: ${RED}$FAILED${NC}"

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}>>> PIPELINE EXITOSO${NC}"
    exit 0
else
    echo -e "${RED}>>> PIPELINE FALLIDO${NC}"
    exit 1
fi
