# Actividad 5: Construyendo un pipeline DevOps con Make y Bash

## Parte 1: Construir - Makefile y Bash desde cero

### Ejercicios

1. **Ejecuta make help y guarda la salida para análisis. Luego inspecciona .DEFAULT_GOAL y .PHONY dentro del Makefile.**

    * El comando make help imprime la lista de los objetivos disponibles y su descripción, facilitando el uso del Makefile. Al declarar **.DEFAULT_GOAL := help**, se configura para que al ejecutar make sin argumentos se muestre la ayuda por defecto. La declaracion de **.PHONY** sirve para indicar que ciertos objetivos no corresponden a archivos lo que evita conflictos si existen archivos con el mismo nombre.

2.  **Comprueba la generación e idempotencia de build. Limpia salidas previas, ejecuta build, verifica el contenido y repite build para constatar que no rehace nada si no cambió la fuente.**

    * En la primera ejecucion de make build, se generan los archivos de salida porque no existen previamente y en la segunda ejecucion make detecta que las dependencias no han cambiado y gracias a las marcas de tiempo no rehace nada, esto demuestra como Make utiliza el grafo de dependencias y los timestamps para evitar trabajo innecesario.

3. **Fuerza un fallo controlado para observar el modo estricto del shell y .DELETE_ON_ERROR. Sobrescribe PYTHON con un intérprete inexistente y verifica que no quede artefacto corrupto.**

    * Al forzar un fallo con un interprete inexistente y usar -e -u -o pipefail, el shell detiene la ejecucion ante errores, variables indefinidas o fallos en tuberias. La directiva .DELETE_ON_ERROR asegura que si ocurre un error los archivos generados parcialmente se eliminan lo que evita que queden artefactos corruptos lo que mantiene el estado consistente.

4. **Realiza un "ensayo" (dry-run) y una depuración detallada para observar el razonamiento de Make al decidir si rehacer o no.**

    * El dry-run (make -n) muestra que acciones se ejecutarian sin realizarlas, permitiendo anticipar cambios. La depuracion (make -d) detalla el proceso de decision de Make mostrando como evalua dependencias, marcas de tiempo y reglas para determinar si debe rehacer un objetivo.

5. **Demuestra la incrementalidad con marcas de tiempo. Primero toca la fuente y luego el target para comparar comportamientos.** 

    * Al modificar la fuente (touch src/hello.py) Make detecta que el archivo fuente es mas reciente que el objetivo y rehace la salida, en cambio al tocar solo el target (out/hello.txt) no se fuerza trabajo extra porque las dependencias no han cambiado, Make considera que el objetivo sigue actualizado respecto a la fuente lo qu emuestra la incrementalidad y eficiencia de Make.

6. **Ejecuta verificación de estilo/formato manual (sin objetivos lint/tools). Si las herramientas están instaladas, muestra sus diagnósticos; si no, deja evidencia de su ausencia.**

    * Si las herramientas shellcheck y shfmt no estan instaladas, los archivos de log mostraran su ausencia y se recomienda instalarlas con los comandos choco install shellcheck segun el sistema. Si estan presentes entonces shellcheck reporta advertencias sobre las buenas practicas y posibles errores en scripts y mientras shfmt sugiere correcciones de formato para mantener un estilo consistente y legible.

7. **Construye un paquete reproducible de forma manual, fijando metadatos para que el hash no cambie entre corridas idénticas.**

    * El hash SHA256 del archivo comprimido reproducible es identico en ambas ejecuciones si no cambio el contenido, esto se logra porque --sort=name ordena los archivos, --mtime='@0' fija la fecha de modificacion, --owner=0 --group=0 --numeric-owner normalizan los metadatos de propietario, y gzip -n evita guardar la fecha en el encabezado, asi se elimina la variabilidad y el empaquetado es verdaderamente reproducible.

8. **Reproduce el error clásico "missing separator" sin tocar el Makefile original. Crea una copia, cambia el TAB inicial de una receta por espacios, y confirma el error.**

    * Make exige un TAB al inicio de cada linea de receta para distinguir comandos de reglas y variables, si se usan espacios se produce el error "missing separator", que puede diagnosticarse rapidamente revisando el mensaje de error y verificando en el Makefile, este error es comun al editar Makefiles en editores que reemplazan TAB por espacios automaticamente.

## Parte 2: Leer - Analizar un repositorio completo

**Ejercicios:**
1. **Ejecuta `make -n all` para un dry-run que muestre comandos sin ejecutarlos; identifica expansiones `$@` y `$<`, el orden de objetivos y cómo `all` encadena `tools`, `lint`, `build`, `test`, `package`.**

    * El comando make -n all muestra los comandos que se ejecutarian, sin realizarlos. Se observan expansiones y el orden de ejecucion sigue la cadena all -> tools -> lint -> build -> test -> package encadenando cada tarea segun sus dependencias.

2. **Ejecuta `make -d build` y localiza líneas "Considerando el archivo objetivo" y "Debe deshacerse",  explica por qué recompila o no `out/hello.txt` usando marcas de tiempo y cómo `mkdir -p $(@D)` garantiza el directorio.**

    * En make -d build, las lineas "Considerando el archivo objetivo" y "Debe deshacerse" indican si out/hello.txt debe recompilarse segn las marcas de tiempo de sus dependencias. El uso de `mkdir -p $(@D)` asegura que el directorio de destino exista antes de crear el archivo lo que evita errores por rutas inexistentes.

3. **Fuerza un entorno con BSD tar en PATH y corre `make tools`; comprueba el fallo con "Se requiere GNU tar" y razona por qué `--sort`, `--numeric-owner` y `--mtime` son imprescindibles para reproducibilidad determinista.**

    * Si BSD tar esta en PATH make tools falla con "Se requiere GNU tar" porque opciones como --sort, --numeric-owner y --mtime no estan disponibles en BSD tar. Estas opciones son esenciales para garantizar que el empaquetamiento sea determinista y reproducible y eliminando variabilidad en los metadatos.

4. **Ejecuta `make verify-repro`; observa que genera dos artefactos y compara `SHA256_1` y `SHA256_2`. Si difieren, hipótesis: zona horaria, versión de tar, contenido no determinista o variables de entorno no fijadas.**

    * Al ejecutar make verify-repro se generan dos artefactos y se comparan sus hashes SHA256_1 y SHA256_2, si difieren o posibles causas incluyen diferencias de zona horaria como version de tar, contenido no determinista o variables de entorno no fijadas, afectan
     la reproducibilidad.

5. **Corre `make clean && make all`, cronometrando; repite `make all` sin cambios y compara tiempos y logs. Explica por qué la segunda es más rápida gracias a timestamps y relaciones de dependencia bien declaradas.**

    * Tras make clean && make all, la primera ejecucion toma mas tiempo porque recompila todo, al repetir make all sin cambios la ejecucion es mas rapida ya que los timestamps y dependencias bien declaradas permiten a Make saltar tareas innecesarias lo que optimizando el proceso.

6. **Ejecuta `PYTHON=python3.12 make test` (si existe). Verifica con `python3.12 --version` y mensajes que el override funciona gracias a `?=` y a `PY="${PYTHON:-python3}"` en el script; confirma que el artefacto final no cambia respecto al intérprete por defecto.**

    * Ejecutar PYTHON=python3.12 make test usa el interprete especificado, lo que se confirma con python3.12 --version y mensajes en el log, el override funciona gracias a la asignacion condicional ?= y a PY="${PYTHON:-python3}" en el script y el artefacto final no cambia respecto al interprete por defecto si el codigo es compatible.

7. **Ejecuta `make test`; describe cómo primero corre `scripts/run_tests.sh` y luego `python -m unittest`. Determina el comportamiento si el script de pruebas falla y cómo se propaga el error a la tarea global.**

    * Al correr make test, primero se ejecuta scripts/run_tests.sh y luego python -m unittest, si el script de pruebas falla el error se propaga y la tarea global tambien falla, deteniendo el proceso y mostrando el diagnostico correspondiente.

8. **Ejecuta `touch src/hello.py` y luego `make all`; identifica qué objetivos se rehacen (`build`, `test`, `package`) y relaciona el comportamiento con el timestamp actualizado y la cadena de dependencias especificada.**

    * Tras modificar src/hello.py y ejecutar make all se rehacen los objetivos build, test y package porque el timestamp actualizado de la fuente desencadena la cadena de dependencias, asegurandose que todo este sincronizado con los cambios.

9. **Ejecuta `make -j4 all` y observa ejecución concurrente de objetivos independientes; confirma resultados idénticos a modo secuencial y explica cómo `mkdir -p $(@D)` y dependencias precisas evitan condiciones de carrera.**

    * Con make -j4 all, los objetivos independientes se ejecutan en paralelo lo que acelera el proceso, los resultados son identicos al modo secuencial y el uso de mkdir -p $(@D) junto con dependencias precisas evita errores de concurrencia.

10. **Ejecuta `make lint` y luego `make format`; interpreta diagnósticos de `shellcheck`, revisa diferencias aplicadas por `shfmt` y, si está disponible, considera la salida de `ruff` sobre `src/` antes de empaquetar.**

    * Ejecutar make lint y luego make format permite revisar advertencias de shellcheck y ver las diferencias de formato aplicadas por shfmt, si ruff esta disponible, su salida sobre src/ ayuda a detectar problemas de estilo en Python antes de empaquetar lo que mejora la calidad del codigo.


## Parte 3: Extender


1. **Usa **GNU tar** para reproducibilidad: `--sort=name`, `--numeric-owner`, `--owner=0`, `--group=0`, `--mtime='UTC 1970-01-01'`. Verifica artefactos con `sha256sum` (GNU coreutils). Evita BSD tar: carece de estos flags y rompe hashes en CI portables.**

    * GNU tar permite reproducibilidad usando --sort=name, --numeric-owner, --owner=0, --group=0 y --mtime='UTC 1970-01-01', asegurando que los artefactos tengan hashes idénticos con sha256sum. BSD tar no soporta estos flags, lo que rompe la portabilidad y la verificación en CI.

2. **Mantén `ruff` como opcional mediante *guard clause*: `command -v ruff >/dev/null && ruff check src || echo "ruff no instalado"`; evita fallos cuando no está disponible y continúa la build, reportando su ausencia.**

    * Ruff debe ejecutarse de forma opcional con una guard clause: command -v ruff >/dev/null && ruff check src || echo "ruff no instalado". Así, si ruff no está instalado, la build continúa y se reporta su ausencia sin fallos.

3. **En WSL, trabaja en `~/proyecto` (o cualquier ruta Linux). Evita `/mnt/c` por I/O lento y diferencias de permisos; mejora tiempos y estabilidad de herramientas.**

    * En WSL es recomendable trabajar en ~/proyecto y evitar /mnt/c ya que el acceso en la ruta nativa de Linux es mas rapido y estable y se evitan problemas de permisos y lentitud que podrian afectar herramientas.

4. **El paralelismo con `make -j` es seguro porque cada receta crea su directorio objetivo con `mkdir -p $(@D)` y las dependencias evitan carreras.**

    * El paralelismo con `make -j` es seguro porque cada receta crea su directorio con `mkdir -p $(@D)` y las dependencias bien definidas previenen condiciones de carrera, garantizando builds consistentes.

5. **Incluye `out/`, `dist/`, `.ruff_cache/` y `**/__pycache__/` en `.gitignore` para evitar artefactos generados en commits y reducir ruido en diffs.**

    * Es importante incluir out/, dist/, .ruff_cache/ y **/pycache/ en .gitignore para evitar que artefactos generados se incluyan en commits manteniendo el repositorio limpio.

6. **Define (si te interesa CI) un objetivo `ci` que encadene `tools`, `check`, `package` y `verify-repro`; así validas dependencias, pruebas, empaquetado y reproducibilidad antes de subir cambios o crear tags.**

    * Para CI, conviene definir un objetivo ci que encadene tools, check, package y verify-repro, validando dependencias, pruebas, empaquetado y reproducibilidad antes de subir cambios o crear tags.

7. **Para probar determinismo y detectar variables "fantasma", usa entornos mínimos: `env -i LC_ALL=C LANG=C TZ=UTC make ...`.**

    * Para probar determinismo y detectar variables ocultas, usa entornos minimos con `env -i LC_ALL=C LANG=C TZ=UTC make ...`  asegurando que la build sea reproducible y libre de efectos colaterales.


## Incidencias y mitigaciones: cualquier problema y cómo lo resolviste.

* Durante la instalacion de herramientas como shellcheck, shfmt y ruff tuve problemas de permisos insuficientes y rutas no incluidas en el PATH. Lo resolvi ejecutando los instaladores con privilegios de administrador y añadiendo las rutas correspondientes al PATH. 
* En WSL detecte lentitud al trabajar en /mnt/c, por lo que migre el proyecto a ~/proyecto para mejorar el rendimiento. 
* Al usar BSD tar en vez de GNU tar, los hashes no coincidian, la solucion fue instalar GNU tar y ajustar el PATH. 


## Conclusión operativa:

* El pipeline es apto para CI/CD porque garantiza reproducibilidad, deteccion temprana de errores y limpieza de artefactos, facilitando integraciones automaticas y despliegues confiables, ademas, la validacion de dependencias y pruebas asegura calidad y consistencia en cada entrega.
