# Evidencia de Laboratorio: DevSecOps con Docker y Airflow

## Resumen de Evidencia
Este archivo va contener la documentación y registros de ejecución que validan la implementación de prácticas DevSecOps en un entorno de ETL con Airflow y Docker.

*   **Construcción y Red:** `00_build.txt` confirma la construcción exitosa de imágenes. `04_topologia.md` y `05_net_inspect.txt` detallan la arquitectura de red aislada (`backend`) y la exposición mínima de puertos.
*   **Salud y Resiliencia:** `10_health_status.txt` muestra el estado `healthy` de los servicios. `10_compose_diff.md` explica la implementación de `healthcheck` y `depends_on` para un arranque ordenado.
*   **Seguridad en Runtime:** `12_user_check.txt` valida que el contenedor de aplicación corre como usuario no-root (`etluser`). `13_env_audit.txt` demuestra la inyección segura de configuración y redacción de secretos.
*   **Supply Chain Security:** `21_sbom.spdx.json` es el inventario de software (SBOM) generado con Syft. `22_scan.txt` es el reporte de vulnerabilidades de Grype. `23_cve_plan.md` propone un plan de remediación para hallazgos críticos.
*   **Operación de Airflow:** `30_dag_resumen.md` documenta el pipeline. `31_dag_run.txt` registra la ejecución exitosa del DAG. `32_timeout_diff.md` detalla la mejora de disponibilidad mediante timeouts.

## Cómo Reproducir
Para levantar el entorno completo desde cero:

1.  **Preparar entorno:**
    ```bash
    cp .env.example .env
    mkdir -p airflow/logs airflow/dags app/data
    chmod -R 777 airflow/logs  # Necesario para el contenedor de Airflow
    ```
2.  **Construir e Inicializar:**
    ```bash
    make build
    make reset-init  # Inicializa la DB de Airflow
    ```
3.  **Arrancar servicios:**
    ```bash
    make up
    ```
4.  **Verificar:** Acceder a `http://localhost:8080` (admin/admin).

## Decisiones de Seguridad Clave
1.  **Principio de Menor Privilegio (Usuario):** Se creó un usuario `etluser` (UID 10001) en el Dockerfile de `etl-app` para evitar la ejecución como `root`, mitigando riesgos de escape del contenedor.
2.  **Aislamiento de Red:** Se utilizó una red `bridge` definida por usuario (`backend`). Solo `airflow-webserver` expone puerto al host; la base de datos y workers se comunican internamente por DNS.
3.  **Límites de Recursos:** Se configuraron límites de CPU y Memoria en `docker-compose.yml` para prevenir denegación de servicio por agotamiento de recursos.
4.  **Healthchecks:** Se implementaron verificaciones de salud (`pg_isready`, script python) para asegurar que el tráfico solo se dirija a contenedores listos.

## Pruebas y Gates de Seguridad
El proyecto incluye comandos `make` para integrar seguridad en el ciclo de desarrollo:

*   **Pruebas Funcionales:**
    ```bash
    make test  # Ejecuta pytest en un entorno aislado
    ```
*   **Generación de SBOM:**
    ```bash
    make sbom  # Genera inventario de software con Syft
    ```
*   **Escaneo de Vulnerabilidades:**
    ```bash
    make scan  # Busca CVEs conocidos con Grype
    ```

## Retos y Validación
Durante la actividad se resolvieron varios desafíos técnicos:
*   **Permisos de Volúmenes:** Se solucionó el error `Permission denied` en `airflow/logs` ajustando los permisos del host para coincidir con el UID del contenedor.
*   **Conectividad de Base de Datos:** Se resolvió la falta de conexión del scheduler asegurando que el servicio `postgres` estuviera `healthy` antes del arranque de dependientes.
*   **Ejecución de DAGs:** Se corrigió el ID del DAG (`etl_pipeline` vs `etl_pipeline_demo`) para permitir la ejecución manual vía CLI.
*   **Resiliencia:** Se añadió un `execution_timeout` de 5 minutos al DAG para evitar tareas zombies, validando la modificación en el código fuente.
