# Topología de Red y Seguridad

## Redes y Aislamiento
El proyecto implementa una arquitectura de red basada en una **user-defined bridge network** denominada `backend`. A diferencia de la red bridge por defecto de Docker, esta red personalizada proporciona aislamiento automático del tráfico (los contenedores fuera de esta red no pueden acceder a los servicios) y habilita la resolución de nombres DNS automática entre contenedores.

## Servicios y Relaciones
La topología se compone de los siguientes servicios interconectados:

1.  **postgres**: Base de datos central. Actua como servidor para `airflow-webserver`, `airflow-scheduler` y `etl-app`.
2.  **airflow-webserver**: Interfaz grafica de Airflow. Se conecta a `postgres` para gestionar el estado de los DAGs y usuarios.
3.  **airflow-scheduler**: Planificador de tareas. Requiere conexion persistente a `postgres` para orquestar ejecuciones.
4.  **etl-app**: Contenedor efimero de procesamiento. Se conecta a `postgres` para insertar los datos transformados.

## Puertos y Exposicion
*   **airflow-webserver (8080:8080)**: Es el único servicio con puerto publicado, necesario para permitir el acceso de los usuarios a la interfaz de gestión.
*   **postgres, etl-app, airflow-scheduler**: Estos servicios no exponen puertos al host (`127.0.0.1` o `0.0.0.0`). 

**Justificación de Seguridad:**
Siguiendo el principio de **menor privilegio**, se restringe la exposición de la base de datos y los workers. `postgres` solo necesita ser accedido por los servicios de la red `backend`, no por usuarios externos ni otros procesos del host. Exponer el puerto 5432 innecesariamente aumentaría la superficie de ataque (fuerza bruta, exploits). De igual forma, `etl-app` y `scheduler` son procesos internos que no requieren interacción directa vía red desde el exterior.

## DNS Interno
La comunicacion entre servicios se realiza exclusivamente mediante **nombres de servicio** (e.g., `postgres`, no IPs). El DNS interno de Docker en la red `backend` resuelve automaticamente `postgres` a la direccion IP interna del contenedor de base de datos, facilitando la configuracion y manteniendo la portabilidad del entorno sin depender de IPs estaticas.
