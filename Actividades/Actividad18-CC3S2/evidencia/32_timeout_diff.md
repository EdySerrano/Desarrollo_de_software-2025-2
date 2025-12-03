# Timeout aplicado a tareas críticas

- Archivo: `airflow/dags/etl_dag.py`
- Cambio: se agregó `execution_timeout=timedelta(minutes=5)` a la tarea `run_etl`.
- Razón: evitar colgados. 5 min es razonable para fuentes locales/CSV. Si se excede, la tarea falla de forma explícita, acelera diagnóstico y evita consumo infinito de recursos.
- Impacto: el scheduler marca la tarea como `failed` si supera el timeout, liberando el worker para otras tareas.
