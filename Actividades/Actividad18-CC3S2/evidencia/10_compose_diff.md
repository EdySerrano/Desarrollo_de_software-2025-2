# Cambios en Docker Compose: Healthchecks y Dependencias

## Cambios
Se han añadido configuraciones de `healthcheck` y condiciones de dependencia (`depends_on`) en el archivo `docker-compose.yml` para mejorar la resiliencia y el orden de arranque de los servicios.

## Detalle de Implementación

### 1. Healthcheck en Postgres
Se añadió un chequeo de salud nativo para la base de datos:
```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
  interval: 10s
  timeout: 5s
  retries: 5
```
**Justificación:**
*   **Verificación Real:** `pg_isready` confirma que la base de datos no solo está corriendo, sino que está lista para aceptar conexiones.
*   **Prevención de Errores:** Evita que los servicios dependientes intenten conectarse antes de que la DB esté operativa.

### 2. Healthcheck en ETL App
Se implementó un script personalizado de salud:
```yaml
healthcheck:
  test: ["CMD", "python", "healthcheck.py"]
  interval: 30s
  timeout: 5s
  retries: 3
```
**Justificación:**
*   **Lógica de Negocio:** Permite verificar condiciones específicas de la aplicación (acceso a archivos, conectividad) más allá de un simple ping.

### 3. Dependencias Condicionales (`depends_on`)
Se actualizaron las dependencias de `etl-app`, `airflow-webserver`, `airflow-scheduler` y `airflow-init` para esperar explícitamente a que Postgres esté saludable:
```yaml
depends_on:
  postgres:
    condition: service_healthy
```
**Justificación:**
*   **Orquestación Robusta:** Garantiza que ningún servicio intente iniciar sus procesos de conexión a base de datos hasta que el healthcheck de Postgres haya pasado exitosamente (`healthy`). Esto elimina las condiciones de carrera durante el arranque del stack ("race conditions") y reduce los reinicios por fallos de conexión iniciales.
