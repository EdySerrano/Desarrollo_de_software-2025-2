# Resumen Operativo del DAG: `etl_pipeline_demo`

## Tareas y Flujo
El DAG consta de una única tarea principal (`run_etl`) implementada mediante `PythonOperator`. Internamente, esta tarea orquesta la lógica del pipeline definida en `app/pipeline.py`:
1.  **Extract**: Lee datos desde un archivo CSV.
2.  **Transform**: Calcula el cuadrado de los valores (`value_squared`).
3.  **Load**: Inserta los registros procesados en la tabla `processed_data` de PostgreSQL.

Flujo lógico interno: `extract() -> transform() -> load()`.

## Configuración
El pipeline sigue la metodología 12-Factor App, configurándose exclusivamente mediante **Variables de Entorno** inyectadas en el contenedor (no utiliza Airflow Connections en esta versión):

*   **Entrada de Datos:**
    *   `ETL_INPUT`: Ruta del archivo CSV origen (Default: `data/input.csv`).
*   **Base de Datos (Destino):**
    *   `POSTGRES_HOST`: Host de la base de datos (e.g., `postgres`).
    *   `POSTGRES_PORT`: Puerto (Default: `5432`).
    *   `POSTGRES_DB`: Nombre de la base de datos.
    *   `POSTGRES_USER`: Usuario.
    *   `POSTGRES_PASSWORD`: Contraseña.

## Ejecución y Monitoreo
*   **Cómo correrlo:**
    *   Automáticamente: Según el schedule `@daily`.
    *   Manual: Desde la UI de Airflow, botón "Trigger DAG" en `etl_pipeline_demo`.
*   **Logs:**
    *   Se registran en la carpeta `airflow/logs/dag_id=etl_pipeline_demo/run_id=.../task_id=run_etl/`.
    *   Accesibles desde la UI: Click en la tarea -> "Log".
*   **Detección de Estado:**
    *   **Éxito:** La tarea termina con código de salida 0. En la UI aparece en verde oscuro ("success"). Verificar datos en DB: `SELECT * FROM processed_data;`.
    *   **Fallo:** Cualquier excepción (falta de archivo, error de conexión DB) propaga un error, marcando la tarea en rojo ("failed"). El traceback completo estará disponible en la pestaña "Log".
