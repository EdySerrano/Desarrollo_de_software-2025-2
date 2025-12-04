# Actividad 20 - CC3S2 RESUMEN

## Parte A - Mejoras en Kubernetes

### A.1. Contenedores y variables

Se han actualizado los manifiestos de Kubernetes para `user-service` y `order-service` con las siguientes mejoras:

1.  **Nombre del contenedor**: Se verifico que los nombres sean `user-service` y `order-service` respectivamente.
2.  **Imagen parametrizable**: Se reemplazo la imagen hardcodeada por `IMAGE_PLACEHOLDER` para permitir la sustitución dinamica desde el pipeline.
3.  **Puertos**: Se confirmaron los puertos `8000` para `user-service` y `8001` para `order-service`.
4.  **Variables de entorno**:
    *   Se aseguro la presencia de la variable `PORT`.
    *   Se añadió la variable `SERVICE_NAME` con el valor correspondiente a cada servicio.

**Archivos modificados:**
*   `Laboratorio11/k8s/user-service/deployment-and-service.yaml`
*   `Laboratorio11/k8s/order-service/deployment-and-service.yaml`

### A.2. Probes de salud

Se han configurado los `livenessProbe` y `readinessProbe` para ambos servicios:

*   **Path**: Se actualizó a `/health`.
*   **Puertos**: `8000` para `user-service` y `8001` para `order-service`.
*   **Tiempos**:
    *   `readinessProbe`: `initialDelaySeconds: 5`, `periodSeconds: 10`.
    *   `livenessProbe`: `initialDelaySeconds: 10`, `periodSeconds: 15`.

Esto asegura que Kubernetes pueda monitorear correctamente el estado de la aplicación y reiniciar los contenedores si es necesario, con tiempos de espera para el inicio de la aplicación.

### A.3. Recursos y seguridad

Se han añadido restricciones de recursos y contexto de seguridad para endurecer los contenedores:

*   **Resources**:
    *   `requests`: cpu: "50m", memory: "64Mi"
    *   `limits`: cpu: "200m", memory: "128Mi"
*   **Security Context**:
    *   `runAsNonRoot: true`: Evita que el contenedor corra como root.
    *   `runAsUser: 1000`: Se alinea con el usuario `app` definido en el Dockerfile.
    *   `allowPrivilegeEscalation: false`: Para prevenir la escalada de privilegios.
    *   `readOnlyRootFilesystem: true`: Monta el sistema de archivos raíz como solo lectura para mayor seguridad.

### A.4. Nombre de namespace

Se recomienda el uso de un namespace dedicado para aislar los recursos. Aunque no se ha forzado en los manifiestos para mantener la compatibilidad con scripts existentes, se sugiere aplicar los manifiestos usando:

```bash
kubectl apply -f Laboratorio11/k8s/user-service/deployment-and-service.yaml -n devsecops-lab11
kubectl apply -f Laboratorio11/k8s/order-service/deployment-and-service.yaml -n devsecops-lab11
```

## Parte B - Makefile y pipeline DevOps local

### B.1. Local-first: sin proveedores nube ni registries remotos

Adapte el flujo de trabajo para priorizar un entorno local con Minikube, eliminando la dependencia de registros externos.

**Cambios en `Laboratorio11/Makefile`:**
1.  **Soporte para Minikube Docker Daemon**: Se actualice los targets `sbom` y `scan` para utilizar `eval $($(MINIKUBE) docker-env)`, esto permite que herramientas como `syft` y `grype` accedan directamente a las imagenes construidas dentro de Minikube sin necesidad de un registro externo.
2.  **Pipeline Local Completo**: El target `pipeline` ahora apunta a `ci` en lugar de `dev`. Esto asegura que el flujo local incluya pasos críticos de seguridad (SBOM, firma, escaneo) además de la construcción y despliegue.
3.  **Orden de Ejecución**: Se ajustó el target `ci` para iniciar `minikube-up` al principio, garantizando que el entorno esté listo antes de construir o escanear imágenes.

**Cambios en Scripts:**
*   **`scripts/minikube_smoke.sh`**: Se actualizó para verificar el endpoint `/health`, manteniendo la compatibilidad con el flujo local mediante `port-forward`.
*   **`scripts/pipeline.sh`**: Ahora invoca el pipeline completo (target `pipeline` -> `ci`), asegurando que las pruebas de seguridad se ejecuten localmente.
*   **`scripts/muestra_salidas.sh`**: Se añadió la visualización de Pods para un mejor diagnóstico.

Este enfoque nos permite un ciclo de desarrollo "Local-first" robusto, en donde la seguridad y la funcionalidad se validan en un entorno identico al de produccion sin salir de la maquina local.

### B.2. Targets mínimos del Makefile

Se han verificado y mejorado los targets del `Makefile` para cumplir con los requisitos de un flujo de desarrollo completo y local:

1.  **`test`**: Añadi un target `test` que ejecuta pruebas de integracion utilizando `docker compose`.
    *   Utiliza `docker-compose.user.test.yml` o `docker-compose.order.test.yml` segun el servicio.
    *   Verifica que el endpoint `/health` responda correctamente.
    *   Se ejecuta dentro del contexto de Docker de Minikube (`eval $(minikube docker-env)`).
2.  **`dev`**: Inclui el paso `test` en el flujo de desarrollo (`env -> minikube-up -> build -> test -> k8s-prepare -> k8s-apply -> smoke`). Esto asegura que solo las imágenes que pasan las pruebas de integración se desplieguen en el clúster.
3.  **`k8s-prepare`**: Se ajusto el comando `sed` para reemplazar específicamente el marcador `IMAGE_PLACEHOLDER` con la imagen construida, garantizando precision en la generacion de manifiestos.

Con estos cambios, el comando `make dev` ahora ejecuta un ciclo completo: configura el entorno, construye la imagen, ejecuta pruebas de integracion, prepara los manifiestos, despliega en Kubernetes y verifica el estado del servicio, todo localmente.

### B.3. Uso de los scripts de apoyo

He optimizado los scripts auxiliares para mejorar la robustez y la observabilidad del pipeline:

1.  **`scripts/minikube_smoke.sh`**:
    *   **Mecanismo de Reintentos**: Implemente un bucle de espera para asegurar que el pod este en estado `Running` antes de intentar el `port-forward`.
    *   **Verificación de Salud Robusta**: Se añadieron reintentos a la petición `curl` contra `/health` para tolerar tiempos de arranque lentos de la aplicación.
    *   **Limpieza**: Se asegura la terminacion del proceso de `port-forward` al finalizar.

2.  **`scripts/pipeline.sh`**:
    *   **Orquestación Clara**: Añadi mensajes de log para delimitar el inicio y fin del pipeline, mostrando claramente los parametros de ejecucion (`SERVICE`, `SCAN_FAIL_SEVERITY`, `COSIGN_VERIFY`).
    *   **Flujo Completo**: Confirma la ejecucion del target `pipeline` del Makefile, que abarca desde la construccion hasta las pruebas de humo.

3.  **`scripts/muestra_salidas.sh`**:
    *   **Eventos de Kubernetes**: Añadi la visualizacion de los ultimos 10 eventos del namespace (`kubectl get events`), lo cual es crucial para diagnosticar problemas de despliegue rapidamente.
    *   **EndpointSlices**: Se mantiene la visualización de `EndpointSlices` para verificar la conectividad de red interna.