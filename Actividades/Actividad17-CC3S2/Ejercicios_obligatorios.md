# Ejercicio 1: Estrategia de "pruebas unitarias" y "pruebas de contrato" combinadas

## 1. Diseño de módulos declarativos

Para diseñar módulos (`network`, `compute`, `storage`) que puedan probarse de forma aislada y reutilizarse eficazmente, la interfaz debe ser clara, predecible y desacoplada.

### Diseño de Interfaces (Variables y Outputs)

*   **Módulo `network`**:
    *   **Variables**: `vpc_cidr` (string con validación regex), `subnet_configs` (lista de objetos con CIDR y AZ), `tags`.
    *   **Outputs**: `vpc_id`, `public_subnet_ids`, `private_subnet_ids`, `default_security_group_id`.
    *   *Aislamiento*: No debe depender de recursos de cómputo existentes.

*   **Módulo `compute`**:
    *   **Variables**: `instance_type`, `mi_id`, `subnet_id`, `security_group_ids`, `user_data`.
    *   **Outputs**: `instance_ids`, `private_ips`, `public_ips`.
    *   *Aislamiento*: Recibe IDs de red como strings, no objetos complejos de Terraform, facilitando el mocking.

*   **Módulo `storage`**:
    *   **Variables**: `bucket_name_prefix`, `versioning_enabled`, `lifecycle_rules`.
    *   **Outputs**: `bucket_arn`, `bucket_name`, `bucket_domain_name`.

### Convenios de Naming y Estructura

Para garantizar el contrato entre equipos:

1.  **Naming Convention**: `snake_case` para todo.
    *   Variables: Prefijos claros (`vpc_...`, `instance_...`).
    *   Outputs: Sufijos que indiquen el tipo de dato (`..._id`, `..._arn`, `..._name`, `..._list`).
2.  **Estructura de Outputs**:
    *   Preferir devolver **objetos o mapas** en lugar de listas planas cuando hay múltiples atributos relacionados (en lugar de `subnet_ids` y `subnet_cidrs` por separado, un output `subnets` que sea un mapa donde la clave es la AZ o el nombre y el valor un objeto con `id` y `cidr`).
    *   Uso estricto de `description` en cada variable y output para que herramientas como `terraform-docs` generen la documentación del contrato automáticamente.
3.  **Versionado**: Uso de Semantic Versioning (SemVer) en los tags del repositorio del módulo.

## 2. Caso limite sin recursos externos

### Escenarios de Inputs Invalidos

Estos escenarios deben detectarse mediante validaciones en el código HCL (`validation` block) y verificarse con tests.

1.  **Escenario 1 (Network)**: Máscara CIDR inválida.
    *   Input: `vpc_cidr = "10.0.0.0/33"` o `vpc_cidr = "invalid-ip"`.
    *   Detección: Bloque `validation` en la variable con `can(cidrhost(var.vpc_cidr, 0))`.

2.  **Escenario 2 (Compute)**: Número de instancias fuera de rango o cero (si la lógica requiere >0).
    *   Input: `instance_count = 0`.
    *   Detección: Bloque `validation` con `condition = var.instance_count > 0`.

### Herramientas y Comandos

Para validar sintaxis vs. semántica sin desplegar infraestructura real (costoso y lento):

1.  **`terraform validate`**:
    *   *Uso*: Validación de **sintaxis** y consistencia interna de tipos.
    *   *Por qué*: Es el primer paso. Verifica que el HCL esté bien formado y que las referencias a variables existan. No conecta con la nube.

2.  **`terraform plan`**:
    *   *Uso*: Validación **semantica** preliminar.
    *   *Por qué*: Evalua las condiciones de los bloques `validation` en las variables. Si pasamos un input invalido (como el CIDR /33), el `plan` fallará inmediatamente antes de intentar crear nada.

3.  **`terraform test` (Framework nativo)**:
    *   *Uso*: Pruebas unitarias y de integración.
    *   *Por qué*: Permite definir aserciones (`assert`) sobre el plan generado. Podemos simular inputs y verificar que los outputs o valores calculados sean los esperados sin necesidad de un `apply` completo si usamos `command = plan`.

## 3. Métrica de cobertura de contrato

### Método de Cuantificación

El contrato de un módulo Terraform son sus **Outputs**, una metrica util es el **Porcentaje de Outputs Verificados**.

$$ \text{Cobertura de Contrato} = \left( \frac{\text{Nº de Outputs con Aserciones en Tests}}{\text{Nº Total de Outputs Declarados}} \right) \times 100\% $$

Por ejemplo, si el módulo `network` exporta 5 valores (`vpc_id`, `subnet_ids`, etc.) y nuestros tests de contrato (`terraform test`) verifican explícitamente que 3 de ellos no sean nulos y tengan el formato correcto, la cobertura es del 60%.

### Balance Exhaustividad vs. Mantenimiento

No es eficiente probarlo todo:

1.  **Priorizar la Interfaz Pública Crítica**: Validar exhaustivamente los outputs que son consumidos por otros módulos, Si estos cambian o rompen, rompen la infraestructura dependiente.
2.  **Outputs Informativos**: Outputs como "tags generados" o descripciones pueden tener validaciones más laxas (ej. solo verificar que existen) o ignorarse en los tests de contrato estrictos para reducir la fragilidad de los tests ante cambios menores.
3.  **Snapshot Testing**: Para evitar escribir aserciones manuales para cada campo, se puede usar "snapshot testing" (guardar el JSON del output esperado y compararlo), pero esto aumenta el mantenimiento si los valores dinámicos (como IDs generados por la nube) no se mockean correctamente. Es mejor aserciones específicas sobre propiedades clave (regex de un ARN, existencia de una clave en un mapa).

# Ejercicio 2: "Pruebas de integración" entre módulos

## 4.  Secuenciación de dependencias

Para encadenar la ejecución de módulos (`network` -> `compute` -> `storage`) en un test de integracion local sin scripts externos, la mejor estrategia es utilizar un **módulo raíz de prueba (root test module)** o el framework nativo `terraform test`.

1.  **Modulo Raiz de Integracion**:
    *   Crear un directorio `tests/integration` con un `main.tf`.
    *   Instanciar los tres módulos dentro de este mismo `main.tf`.
    *   **Encadenamiento Declarativo**: Pasar los outputs de un modulo directamente como inputs del siguiente. Terraform construye automaticamente el grafo de dependencias (DAG) y determina el orden de creación correcto.
    *   *Ejemplo conceptual*:
        ```hcl
        module "network" { source = "../../modules/network" ... }
        module "compute" {
          source = "../../modules/compute"
          subnet_id = module.network.public_subnet_ids[0] # Dependencia implicita
        }
        module "storage" { source = "../../modules/storage" ... }
        ```

2.  **Garantia de Consumo de Outputs**:
    *   Al usar referencias directas (`module.network.output_name`), Terraform garantiza que `network` se cree antes que `compute`.
    *   **Validación de Tipos**: Terraform fallará durante el `plan` si el tipo de dato del output de `network` no coincide con el tipo esperado por la variable de `compute`, asegurando la integridad del contrato sin scripts "pegamento".

## 5. Entornos simulados con contenedores
### Diseño de Prueba con Docker

Para simular una base de datos (PostgreSQL) y validar conectividad:

1.  **Levantar el Contenedor**:
    *   Usar el provider `kreuzwerker/docker` dentro del mismo codigo de prueba de Terraform para levantar un contenedor de base de datos.
    *   Exponer el puerto del contenedor al host local (o a la red Docker si se ejecuta en CI).

2.  **Conexion con Terraform**:
    *   Pasar la direccion IP y puerto del contenedor (obtenidos del recurso `docker_container`) como variables al módulo `compute`.
    *   Configurar el módulo `compute` o usar un provisioner para intentar conectar a la DB.

3.  **Validacion de Comunicacion**:
    *   Usar un `null_resource` con un `local-exec` o `remote-exec` que ejecute un script simple para verificar que la instancia creada puede alcanzar el servicio simulado.

### Retos de Aislamiento y Limpieza

*   **Reto**: Conflictos de puertos si se ejecutan multiples tests en paralelo, o contenedores huerfanos si Terraform falla antes del destroy.
*   **Mitigación**:
    *   **Puertos Dinámicos**: No fijar puertos en el host. Dejar que Docker asigne un puerto aleatorio y recuperarlo vía output del provider para pasarlo a los tests.
    *   **Nombres Únicos**: Usar `random_id` para generar nombres de contenedores únicos por ejecucion.
    *   **Ephemeral Environments**: Ejecutar los tests dentro de un contenedor efimero (Docker-in-Docker) que se destruye totalmente al finalizar, asegurando limpieza absoluta.

## 6. Pruebas de interaccion gradual

### Nivel 1: Validación de Legibilidad (Smoke Tests / Configuration Tests)
*   **Objetivo**: Verificar que los módulos se conectan correctamente y que los valores fluyen sin errores de tipo o sintaxis.
*   **Alcance**: Ejecutar `terraform plan` o `terraform apply` y verificar que los outputs de `network` se pasan a `compute` y que `compute` no falla al recibirlos.
*   **Uso**: En cada Pull Request (PR) para feedback rapido. Evita errores tontos de configuración.

### Nivel 2: Validacion de Flujo de Datos (Functional / E2E Tests)
*   **Objetivo**: Verificar que la infraestructura hace lo que debe (como escribir en un bucket, conectar a una DB).
*   **Alcance**: Despliegue completo (`terraform apply`). Ejecutar scripts de prueba reales: conectarse por SSH a la instancia y escribir un archivo en el bucket S3 montado, o hacer una query a la DB.
*   **Uso**: En ramas principales (main/develop) o nightly builds. Son costosos y lentos.

### Evitar Solapamientos
*   El **Nivel 1** debe ser un subconjunto rápido del Nivel 2. Si el Nivel 1 falla, no ejecutar el Nivel 2.
*   Usar **tags** en los tests (`unit`, `integration`, `e2e`) para filtrar qué ejecutar.
*   No probar funcionalidades del proveedor de nube, sino probar **nuestra configuración** (permisos IAM correctos, rutas de red correctas).

# Ejercicio 3: "Pruebas de humo" y "Pruebas de regresión"

## 7. Pruebas de humo locales ultrarrápidos

Para una validación rapida (< 30s) antes de cualquier push, ejecutaria:

1.  **`terraform fmt -check -recursive`**:
    *   *Valor*: Asegura consistencia de estilo inmediatamente. Si falla, el código es ilegible o no cumple estándares.
2.  **`terraform validate`**:
    *   *Valor*: Verifica la sintaxis y la validez de las referencias internas (variables, atributos) sin conectar a la nube. Detecta errores tipográficos y de tipos.
3.  **`terraform plan -refresh=false`**:
    *   *Valor*: Genera un plan de ejecución asumiendo que el estado remoto está sincronizado (sin consultar la API real). Valida la lógica de las expresiones y dependencias mucho más rápido que un plan completo.

## 8. Planes "golden" para regresión

### Procedimiento y Detección de Diferencias

1.  **Generación**: Crear un plan base aprobado: `terraform plan -out=tfplan && terraform show -json tfplan > golden-plan.json`.
2.  **Comparación**: En CI, generar un nuevo plan JSON y compararlo con el `golden-plan.json`.
3.  **Evitar Falsos Positivos**:
    *   No comparar los archivos JSON como texto plano.
    *   Usar herramientas como `jq` o scripts (Python/Go) para extraer y comparar solo la sección `resource_changes`.
    *   **Filtrado**: Ignorar campos volátiles o generados dinámicamente como `timestamp`, `uuid` o atributos marcados como `(known after apply)` a menos que su *existencia* sea lo que se prueba.

## 9. Actualización consciente de regresión

### Política de Equipo

*   **Cuándo actualizar**: Los planes dorados solo se regeneran cuando un cambio en la infraestructura es **intencional y aprobado**. No se actualizan para silenciar un test fallido.
*   **Requisito**: "Todo cambio en el `golden-plan.json` requiere aprobación explícita de un Senior/Lead o revisión de 2 pares".

### Criterios de Aprobación

1.  **Intencionalidad**: El `diff` del plan muestra *exactamente* lo que describe la User Story (ej. "Se añade 1 bucket", el plan muestra `+1 aws_s3_bucket`).
2.  **Sin Efectos Secundarios**: No hay modificaciones (`~`) o destrucciones (`-`) en recursos críticos que no estaban previstos.
3.  **Seguridad**: No se exponen nuevos puertos ni se modifican políticas IAM de forma insegura.

# Ejercicio 4: "Pruebas extremo-extremo (E2E)" y su rol en arquitecturas modernas

## 10. Escenarios E2E sin IaC real

### Descripción del Test
1.  **Despliegue**: `terraform apply` levanta una red Docker local, un contenedor simulando un Load Balancer y contenedores backend con la app Flask.
2.  **Verificación**: Un script de prueba (Python con `pytest` y `requests`) se ejecuta desde el host.
3.  **Flujo**: El script lanza peticiones HTTP al puerto expuesto del Load Balancer, verificando que el tráfico llega a los backends (round-robin).

### Métricas e Integración
*   **Métricas**:
    *   **Status Codes**: Esperar `200 OK`. Un `502/503` indica fallo en la conexión LB -> Backend.
    *   **Latencia**: Tiempos de respuesta aceptables (< 100ms) para descartar loops de red.
    *   **Payload**: Validar que el JSON de respuesta contiene la identificacion del backend (para confirmar balanceo).
*   **Integración sin CI externo**:
    *   Utilizar el framework `terraform test` o un `null_resource` con `local-exec` que dispare `pytest` tras el despliegue.
    *   Usar `defer` o bloques de limpieza en el script de prueba para asegurar `terraform destroy` al finalizar, independientemente del resultado.

## 11. E2E en microservicios y Kubernetes local (opcional)

### Diseño con Kind
1.  **Provisioning**: Terraform usa el provider `kind` para levantar un cluster y el provider `helm` para desplegar la aplicacion.
2.  **Validacion**:
    *   **Readiness/Liveness Probes**: Configuradas en los manifiestos. Terraform espera a que los Deployments estén `Ready`.
    *   **Conectividad Interna**: Desplegar un pod "tester" (ej. `curlimages/curl`) mediante un recurso `kubernetes_pod` o `job`. Este pod hace curl a los servicios internos (ClusterIP) para validar que el DNS de K8s y las Network Policies permiten el trafico.

## 12. Simulacion de fallos en E2E

### Introduccion de Fallos
*   **Caida de Pod**: Ejecutar `kubectl delete pod -l app=mi-app` mediante un `local-exec` en Terraform o script auxiliar.
*   **Fallo de Nodo**: Usar `docker stop <kind-worker-node>` para simular la caida de un nodo del cluster.

### Mecanismos y Comprobacion
*   **ReplicaSets/Deployments**: Validar que Kubernetes programa nuevos pods en los nodos disponibles para cumplir el `replicas: N`.
*   **Validacion**:
    *   Sondear el endpoint del servicio continuamente durante el fallo. Debería haber una breve interrupcion o ninguna, pero el servicio debe recuperarse automaticamente.
    *   Comprobar con `kubectl get pods` que los nuevos pods pasan a estado `Running` y `Ready`.

# Ejercicio 5: Pirámide de pruebas y selección de tests

## 13. Mapeo de pruebas al pipeline local

### Secuencia de Ejecucion (Script Local)
Para respetar la pirámide de pruebas (más tests rápidos y baratos en la base, menos tests lentos y caros en la cima):

1.  **Unit Tests & Static Analysis** (Base):
    *   `terraform fmt -check`
    *   `terraform validate`
    *   `tflint`
    *   `terraform test -filter=tests/unit` (validaciones de lógica interna sin providers reales).
2.  **Smoke & Contract Tests**:
    *   `terraform plan`.
    *   Validación de outputs contra esquema JSON esperado (Contract Tests).
3.  **Integration Tests**:
    *   `terraform test -filter=tests/integration` (despliegue de módulos conectados en entorno aislado/sandbox).
4.  **E2E Tests** (Cima):
    *   Despliegue completo de la arquitectura.
    *   Ejecución de scripts de prueba de negocio (peticiones HTTP, queries DB).

### Medicion y Optimizacion
*   **Medicion**: Usar el comando `time` de Unix para cada bloque o registrar timestamps en un log.
*   **Optimización**:
    *   Si la fase de Integración tarda > 5 min, revisar si se pueden mockear recursos lentos.
    *   Si E2E falla a menudo por timeouts, aumentar recursos o mejorar la resiliencia del test (retries).

## 14. Estrategia de "test slices"

### Agrupacion y Ejecucion Independiente
*   **Estructura**: Organizar tests en carpetas `tests/network`, `tests/compute`, `tests/storage`.
*   **Deteccion de Cambios**: Usar `git diff --name-only HEAD~1` para detectar que directorios han cambiado.
*   **Logica de Disparo**:
    *   Si cambia `modules/network/*.tf` -> Ejecutar `tests/network` Y `tests/compute`.
    *   Si cambia `modules/compute/*.tf` -> Ejecutar solo `tests/compute`.

### Criterios
*   **Dependencia Inversa**: Ejecutar tests del modulo modificado y de todos los modulos que dependen de el (downstream).
*   **Scope**: Si el cambio es en `variables.tf` (interfaz), ejecutar contract tests de todos los consumidores. Si es en `main.tf` (implementacion), basta con integration tests del propio modulo.

## 15. Coste vs. riesgo de tests

### Balance y ROI
*   **Heurística**: "Un test E2E debe cubrir un flujo crítico de negocio que, si falla, cuesta dinero inmediato".
*   **Formula de ROI**:
    $$ ROI = \frac{(\text{Probabilidad de Fallo} \times \text{Coste del Incidente}) - \text{Coste de Creación del Test}}{\text{Coste de Mantenimiento Mensual}} $$
*   Si el mantenimiento (arreglar tests flaky) supera el riesgo ponderado, el test debe eliminarse o bajarse de nivel (convertirse en unitario mockeado).

# Ejercicio 6: Estrategias de mantenimiento y evolución de la suite

## 16. Deuda tecnica en pruebas IaC

### Señales de Deuda
1.  **Flakiness**: Tests que fallan aleatoriamente sin cambios en el codigo (falsos positivos).
2.  **Tiempos de Ejecucion Crecientes**: La suite pasa de 5 min a 30 min sin justificacion.
3.  **Código Duplicado**: Mismo setup de provider o variables copiado en 20 archivos de test.

### Plan de Refactorizacion
1.  **Modularizar Tests**: Crear "helper modules" para setups comunes (un módulo `test-setup-vpc` que se reutilice en todos los tests de compute).
2.  **Eliminar Flakiness**: Identificar tests inestables y arreglar la condición de carrera o borrarlos si no aportan valor crítico.
3.  **Priorización**: Empezar por los módulos `core` (network, security) que afectan a todo.

## 17. Documentacion viva de tests

### Formato y Sincronizacion
*   **Formato**: Tabla en `README.md` del modulo o `TESTING.md`.
    *   Columnas: `Test ID`, `Descripción`, `Tipo (Unit/Int/E2E)`, `Inputs Clave`, `Outputs Verificados`.
*   **Alineacion con Code Review**:
    *   Regla: "Ningun PR se aprueba si añade una feature sin su entrada correspondiente en la tabla de tests".
    *   Uso de herramientas como `terraform-docs` para generar partes de la documentacion automaticamente desde descripciones en el codigo.

## 18. Automatizacion local de la suite

### Script Maestro (`run_all.sh`)

```bash
#!/bin/bash
set -e # Detener si hay error crítico, o usar set +e para recoger todos los resultados

LOG_FILE="test_report.log"
echo "Iniciando Suite de Pruebas..." > $LOG_FILE

# Funcion helper
run_phase() {
    phase_name=$1
    cmd=$2
    echo "Ejecutando $phase_name..."
    if eval "$cmd"; then
        echo "$phase_name: PASSED" >> $LOG_FILE
    else
        echo "$phase_name: FAILED" >> $LOG_FILE
        # Notificación local (sonido o alerta visual)
        echo -e "\a" # Beep
        notify-send "Test Fallido" "Fallo en fase: $phase_name" || true
    fi
}

# 1. Limpieza previa
# terraform destroy -auto-approve

# 2. Fases
run_phase "Unit Tests" "terraform validate && terraform fmt -check"
run_phase "Smoke Tests" "terraform plan -refresh=false"
# run_phase "Integration" "terraform test -filter=tests/integration"

# 3. Resumen
echo "----------------RESUMEN----------------"
cat $LOG_FILE
if grep -q "FAILED" $LOG_FILE; then
    echo "SUITE FALLIDA"
    exit 1
else
    echo "SUITE EXITOSA"
    exit 0
fi
```

# Ejercicio 7: Ampliación de módulos y pruebas unitarias "en caliente"

## Tarea A: Modulo Firewall
Diseño de un modulo que abstrae reglas de seguridad.

*   **Inputs**: `rules` (lista de objetos: `{ port: number, cidr: string, protocol: string }`).
*   **Lógica**: Iterar sobre la lista y construir una estructura de datos unificada.
*   **Output**: `policy_json` (string).
    ```hcl
    output "policy_json" {
      value = jsonencode({
        version = "1.0"
        rules   = var.rules
      })
    }
    ```

## Tarea B: Modulo DNS
Diseño de un modulo para gestion de registros.

*   **Inputs**: `records` (mapa de `hostname` -> `ip_address`).
*   **Validacion**: Usar `validation` block con regex para asegurar que las claves son hostnames válidos (sin espacios, caracteres especiales).
*   **Output**: `records_map` (mapa).

## Pruebas Unitarias

1.  **Firewall**:
    *   Crear un test en `tests/firewall.tftest.hcl`.
    *   Definir variables fijas.
    *   Assert: `output.policy_json == jsonencode(...)`. Esto asegura que el formato no cambie accidentalmente.

2.  **DNS (Validacion)**:
    *   Crear un test que inyecte un hostname invalido ("mi servidor").
    *   Assert: Esperar fallo (`expect_failures = [var.records]`).

# Ejercicio 8: Contratos dinámicos y testing de outputs (opcional)

## Tarea A: Esquemas JSON
Definir archivos `.schema.json` para cada modulo.
*   Ejemplo `network.schema.json`:
    ```json
    {
      "type": "object",
      "properties": {
        "vpc_id": { "type": "string", "pattern": "^vpc-[a-z0-9]+$" }
      },
      "required": ["vpc_id"]
    }
    ```

## Tarea B: Driver de Validacion
Script en Python (`validate_outputs.py`):
1.  Ejecutar `terraform output -json > outputs.json`.
2.  Cargar `outputs.json` y los esquemas.
3.  Usar libreria `jsonschema` para validar cada output contra su esquema correspondiente.

## Contrato Evolutivo
*   **Versionado**: Guardar esquemas en carpeta `schemas/v1/`, `schemas/v2/`. El driver lee la version declarada en el output o variable del modulo.
*   **Reporte**: El script debe imprimir una tabla:
    ```text
    Module    | Output      | Status | Error
    ----------|-------------|--------|------
    network   | vpc_id      | PASS   |
    dns       | records_map | FAIL   | Pattern mismatch
    ```

# Ejercicio 9: Integracion encadenada con entornos simulados

## Tarea A: Contenedor Mock en Compute
*   Recurso: `null_resource` o `docker_container` (si se usa el provider).
*   Provisioner `local-exec`: `docker run -d --name mock-db -p 8080:80 hashicorp/http-echo -text="hello"`
*   Obtención de IP: Usar `external` data source o outputs del provider docker para capturar la IP del contenedor.

## Tarea B: Firewall Dinamico
*   El modulo `compute` exporta la IP del contenedor (`mock_db_ip`).
*   El modulo `firewall` recibe esta IP en su variable `rules` o una variable dedicada `trusted_ips`.

## Pruebas de Integracion

1.  **Verificacion de DNS**:
    *   Flujo: `Compute (Docker IP)` -> `Firewall` -> `DNS (registrar mock-db.local -> IP)`.
    *   Validacion: `dig @localhost mock-db.local` o script que lea el output de Terraform y verifique que la IP coincide con `docker inspect`.

2.  **Simulación de Latencia**:
    *   Inyectar fallo: `docker exec mock-db tc qdisc add dev eth0 root netem delay 500ms`.
    *   Logica de Retry: Terraform tiene timeouts configurables en providers, pero para `local-exec` o scripts de validación, implementar bucles `until` en Bash o `retries` en Python para tolerar la latencia inicial.

# Ejercicio 10: Pruebas de humo híbridos con Terraform

## Tarea A: Script `run_smoke.sh`

Este script itera sobre los modulos y ejecuta validaciones rapidas.

```bash
#!/bin/bash
set -e

MODULES_DIR="modules"

for module in $(ls $MODULES_DIR); do
    echo "Testing module: $module"
    cd "$MODULES_DIR/$module"
    
    # 1. Estilo
    terraform fmt -check
    
    # 2. Validacion
    terraform init -backend=false > /dev/null
    terraform validate
    
    # 3. Plan rapido
    # Se requiere un archivo de variables dummy o defaults para que funcione
    terraform plan -refresh=false -out=tfplan > /dev/null
    
    cd - > /dev/null
done
echo "Smoke tests pasaron!"
```

## Tarea B: Comprobacion de Contrato Minima

Añadir al script la extraccion y verificacion de un output clave.

```bash
# ... dentro del loop ...
terraform show -json tfplan > tfplan.json

# Verificar existencia de key
SUBNET_COUNT=$(jq '[.resource_changes[] | select(.type == "aws_subnet")] | length' tfplan.json)

if [ "$SUBNET_COUNT" -eq "0" ] && [ "$module" == "network" ]; then
    echo "Error: Network module debe crear subnets"
    exit 1
fi
```

# Ejercicio 11: Pruebas de integración con "plan dorado" inteligentes 

## Tarea A: Generación de Planes Base

Para `network` y `firewall`:
1.  Crear `tests/fixtures/network.tfvars` con valores estables.
2.  Ejecutar:
    ```bash
    terraform plan -var-file=tests/fixtures/network.tfvars -out=base.tfplan
    terraform show -json base.tfplan > tests/goldens/network.json
    ```

## Tarea B: Script de Comparación Inteligente

Script `compare_plans.sh`:

```bash
#!/bin/bash
GOLDEN=$1
NEW_PLAN_JSON=$2

# Normalizar
normalize() {
    jq 'del(.timestamp, .terraform_version, .variables, .planned_values.root_module.resources[].values.id)' $1 | \
    jq --sort-keys .resource_changes
}

diff <(normalize $GOLDEN) <(normalize $NEW_PLAN_JSON)

if [ $? -eq 0 ]; then
    echo "No hay cambios semanticos detectados."
else
    echo "Cambios detectados contra el Plan."
fi
```

## Política de Actualización

*   **Cuándo**: Solo tras cambios funcionales aprobados (Feature Releases) o correcciones de bugs que alteren la infraestructura. Nunca en refactors puros.

# Ejercicio 12: Flujo E2E local con microservicios simulados

## Tarea A y B: Despliegue de Microservicios

Usar `docker_container` en Terraform.

*   **Backend (Flask)**: Red interna `backend_net`. No expuesto al host.
*   **Frontend (Nginx)**: Red interna `backend_net` y puerto expuesto `8080:80`. Configurado como proxy reverso hacia el nombre del contenedor backend.

## Pruebas E2E

Script de validación `verify_e2e.py`:

1.  **Frontend Root**:
    ```python
    resp = requests.get("http://localhost:8080/")
    assert resp.status_code == 200
    ```
2.  **Backend Directo (Aislamiento)**:
    ```python
    # Asumiendo que no mapeamos puerto del backend
    try:
        requests.get("http://localhost:5000/api/status", timeout=2)
        assert False, "Backend should not be reachable directly"
    except requests.exceptions.ConnectionError:
        pass
    ```
3.  **Frontend -> Backend**:
    ```python
    resp = requests.get("http://localhost:8080/api/data")
    assert resp.json() == {"data": "from_backend"}
    ```

## Prueba de Recuperacion (Idempotencia)

1.  `terraform destroy -target=module.compute`
2.  `terraform apply -auto-approve`
3.  Re-ejecutar `verify_e2e.py`.
    *   Esto valida que `network` y `firewall` persisten y que `compute` se reconecta correctamente a la infraestructura existente.
