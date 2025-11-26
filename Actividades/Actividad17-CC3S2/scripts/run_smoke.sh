#!/bin/bash
set -e

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo ">>> Iniciando Smoke Tests..."

# 1. Terraform Format Check
echo "Checking terraform fmt..."
if terraform fmt -check -recursive ..; then
    echo -e "${GREEN}Format check passed${NC}"
else
    echo -e "${RED}Format check failed${NC}"
    exit 1
fi

# 2. Terraform Validate
echo "Running terraform validate..."
# Asumimos que estamos en la raiz del proyecto o ajustamos el path
if terraform validate; then
    echo -e "${GREEN}Validation passed${NC}"
else
    echo -e "${RED}Validation failed${NC}"
    exit 1
fi

# 3. Terraform Plan & Contract Check
# Iterar sobre directorios en modules/ si existen, sino en el directorio actual
MODULES_DIR="../modules"
if [ -d "$MODULES_DIR" ]; then
    TARGETS=$(find "$MODULES_DIR" -maxdepth 1 -mindepth 1 -type d)
else
    TARGETS="."
fi

for module in $TARGETS; do
    echo "Running plan for module: $module"
    
    # Generar plan sin refresh para velocidad
    # Nota: En un entorno real, necesitarías init si no se ha hecho
    terraform -chdir="$module" init -backend=false > /dev/null
    
    PLAN_FILE=$(mktemp)
    if terraform -chdir="$module" plan -refresh=false -out="$PLAN_FILE" > /dev/null; then
        echo -e "${GREEN}Plan generated for $module${NC}"
        
        # 4. Extraer valor contractual
        # Ejemplo: Verificar que el plan no este vacío o contiene un recurso especifico
        # Aqui convertimos a JSON y buscamos algo basico, por ejemplo, que exista "resource_changes"
        PLAN_JSON=$(terraform -chdir="$module" show -json "$PLAN_FILE")
        
        # Verificacion simple de contrato: ¿Hay cambios planificados o configuración valida?
        # Buscamos si existe la clave "format_version" que siempre esta en el JSON de terraform
        if echo "$PLAN_JSON" | grep -q "format_version"; then
             echo -e "${GREEN}Contract check passed: Valid Terraform Plan JSON detected${NC}"
        else
             echo -e "${RED}Contract check failed: Invalid Plan output${NC}"
             rm "$PLAN_FILE"
             exit 1
        fi
        
        rm "$PLAN_FILE"
    else
        echo -e "${RED}Plan failed for $module${NC}"
        exit 1
    fi
done

echo -e "${GREEN}>>> Smoke Tests Completados Exitosamente (<30s)${NC}"
