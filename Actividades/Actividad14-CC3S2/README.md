## Actividad14 - CC3S2

Este directorio contiene las soluciones de la actividad 14 organizadas en fases (Fase1, Fase2, Fase3). Cada fase agrupa ejercicios que implementan patrones de diseño aplicados a Infraestructura como Código (IaC), utilidades para generar JSON compatibles con Terraform y pruebas automatizadas.

### Estructura principal

- `Fase1/` — Documentacion y entregables conceptuales:
	- Contiene la explicacion de los patrones (Singleton, Factory, Prototype, Composite) y diagramas/entregables que muestran el diseño de la solucion.
	- Archivos clave: `Entregable_Fase1.md`, diagramas y notas.

- `Fase2/` — Implementaciones practicas por ejercicio (código que genera ejemplos `.tf.json`):
	- `Ejercicio2.1/` — `singleton.py`: metaclase `SingletonMeta` y `ConfigSingleton`.
	- `Ejercicio2.2/` — `factory.py`: `NullResourceFactory` que construye bloques `null_resource`.
	- `Ejercicio2.3/` — `prototype.py` y ejemplo `welcome.tf.json`: clonacion de prototipos y mutators.
	- `Ejercicio2.4/` — `composite.py` y `submodules.tf.json`: composicion de módulos (CompositeModule).
	- `Ejercicio2.5/` — `builder.py` y `web_group.tf.json`: `InfrastructureBuilder` que orquesta Factory+Prototype+Composite para exportar `main.tf.json`.

- `Fase3/` — Patrones avanzados, adaptadores, tests y análisis:
	- `Ejercicio3.1/` — Análisis conceptual (`Factory_vs_Prototype.md`) y comparativas.
	- `Ejercicio3.2/` — `adapter.py`, `builder.py`, demo y `mock_bucket.tf.json`: ejemplo del patron Adapter que convierte `null_resource` en `mock_cloud_bucket`.
	- `Ejercicio3.3/` — tests con `pytest` (`test_patterns.py`), `prototype.py` y `pytest_results.txt` (suite que valida Singleton y Prototype).
	- `Ejercicio3.4/` — `measure_sizes.py`, `size_log.txt` y `Discusion.md`: script para medir tamaños de `main.tf.json` y discusión sobre escalabilidad en CI/CD.


#### **Artefactos generados**

- Archivos `.tf.json` de ejemplo se colocan en subcarpetas `terraform/` dentro de cada ejercicio.
- Los artefactos generados no son necesarios para el código fuente y pueden regenerarse con los scripts incluidos.

#### **Reproducir localmente (pasos)**

1. Clona el repositorio y sitúate en la carpeta de actividades. (git clone --)
2. Asegúrate de usar Python 3.10+ (el código usa solo la librería estándar salvo `pytest` para tests).
3. Para ejecutar las pruebas del ejercicio 3.3 (pytest): ejecuta `pytest` apuntando a `Fase3/Ejercicio3.3`.
4. Para regenerar ejemplos o medir tamaños (ej. Ejercicio3.4), ejecuta los scripts `builder.py` o `measure_sizes.py` contenidos en los subdirectorios.
