# Conceptualización de Microservicios

La evolución del software ha transitado del Monolito a SOA y finalmente a los Microservicios. Aunque los monolitos facilitan el arranque, se vuelven costosos de operar en escenarios como e-commerce con picos estacionales o SaaS multi-tenant donde el escalado desigual y los despliegues lentos son críticos. Un microservicio es una unidad de despliegue independiente con una capacidad de negocio y contrato API definido; la aplicación es la suma de estos servicios más su infraestructura (gateway, observabilidad).

El monolito sufre de cadencia de despliegue reducida y acoplamiento fuerte. Por ello, empresas líderes adoptaron microservicios para ganar aislamiento de fallos, escalado y autonomía de equipos. No obstante, esto introduce retos en redes/seguridad, orquestación, consistencia de datos y testing distribuido. Estas dificultades se mitigan mediante contratos (OpenAPI), pruebas contractuales, trazabilidad y patrones de sagas.

El diseño efectivo se basa en DDD para definir límites contextuales y en un manejo cuidadoso de DRY, equilibrando librerías comunes frente a una duplicación controlada para reducir acoplamiento. El criterio de tamaño debe ser la capacidad de negocio, evitando dogmas como "una tabla por servicio".
En conclusión, los microservicios son ideales cuando la necesidad de escalabilidad y agilidad justifica la complejidad operativa.

# Empaquetado y verificación con Docker (base obligatoria)

El repositorio de referencia incluye Dockerfile y pruebas. Aquí se describen conceptos y pasos; no se pega código completo.

**Evidencias en texto plano:**

1.  **Build**:
    ```bash
    $ make build
    docker build -t ejemplo-microservice:0.1.0 .
    [+] Building 1.4s (14/14) FINISHED
    ...
    => => naming to docker.io/library/ejemplo-microservice:0.1.0
    ```

2.  **Run**:
    ```bash
    $ make run
    docker run -d -p 80:80 --name ejemplo-microservice ejemplo-microservice:0.1.0
    b071b2a1112fa26171ce13cc2e00f35c01213c4b5565b93f0a407ca41009e4b3
    ```

3.  **Curl** (Probando el endpoint):
    ```bash
    $ curl -L http://localhost:80/api/items
    []
    ```

4.  **Logs**:
    ```bash
    $ docker logs ejemplo-microservice
    INFO:     Started server process [1]
    INFO:     Waiting for application startup.
    2025-12-03 21:01:57,013 - INFO - microservice - Arrancando la aplicación
    2025-12-03 21:01:57,013 - INFO - microservice - Inicializando base de datos en app.db
    INFO:     Application startup complete.
    INFO:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
    INFO:     172.17.0.1:35192 - "GET /api/items HTTP/1.1" 307 Temporary Redirect
    INFO:     172.17.0.1:35192 - "GET /api/items/ HTTP/1.1" 200 OK
    ```

5.  **Pytest** (Ejecutado dentro del contenedor):
    ```bash
    $ docker exec ejemplo-microservice pytest -q
    ..
    2 passed, 8 warnings in 0.72s
    ```

### ¿Por qué no usar latest?

El tag `latest` es un poco ambiguo: no indica versión, cambios ni compatibilidad. Puede romper entornos al actualizarse inesperadamente, ya que un `docker pull` podría traer una versión con cambios disruptivos sin previo aviso.

### SemVer y reproducibilidad

**SemVer (Semantic Versioning - MAJOR.MINOR.PATCH)** permite:

*   **Reproducibilidad**: Al etiquetar una imagen como `0.1.0`, garantizamos que siempre reconstruiremos o desplegaremos exactamente el mismo artefacto, eliminando el "funciona en mi máquina".
*   **Trazabilidad**: Permite saber exactamente qué cambios (commits) introdujo cada versión.
*   **Despliegues seguros**: Facilita la promoción de versiones probadas entre entornos (dev -> staging -> prod), por ejemplo, promoviendo la imagen `0.1.0` inmutable en lugar de reconstruir una "latest" que podría haber cambiado.
