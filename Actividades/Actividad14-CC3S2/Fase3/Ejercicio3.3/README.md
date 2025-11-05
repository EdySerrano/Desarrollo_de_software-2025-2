## Ejercicio 3.3 — Tests automatizados con pytest

Este ejercicio añade pruebas automatizadas para verificar patrones de diseño (Singleton y Prototype) usando `pytest`.

### **Contenido de la carpeta**

- **`prototype.py`**
  - Implementa la clase `ResourcePrototype`, una implementación sencilla del patrón Prototype.
  - `ResourcePrototype` guarda una copia defensiva del template y ofrece `clone(mutator)` que devuelve una nueva instancia con una copia profunda de los datos y aplica un `mutator` in-place si se provee.

- **`test_patterns.py`**
  - Contiene los tests solicitados en la tarea:
    - `test_singleton_meta`: carga dinamicamente `ConfigSingleton` desde `Fase2/Ejercicio2.1/singleton.py` y verifica que dos invocaciones devuelven la misma instancia.
    - `test_prototype_clone_independent`: carga `NullResourceFactory` desde `Fase2/Ejercicio2.2/factory.py`, utiliza `ResourcePrototype` local para clonar un template dos veces con mutators distintos y verifica que las clonaciones son independientes.
  - Para evitar reorganizar los módulos del repositorio, los tests usan `importlib.util.spec_from_file_location` para cargar los modulos por ruta de archivo. Esto mantiene los tests autonomos dentro de `Ejercicio3.3`.

- `pytest_results.txt`
  - Archivo con la salida breve de la ejecución de `pytest` para esta carpeta.

### **Cómo lo implemente?**

1. Implementé `ResourcePrototype` en `prototype.py` usando `deepcopy` para asegurar que cada clon sea independiente del original.
2. Redacte `test_patterns.py` con dos pruebas mínimas pedidas en la tarea, los tests cargan:
   - `ConfigSingleton` desde `Fase2/Ejercicio2.1/singleton.py` para validar el patrón Singleton.
   - `NullResourceFactory` desde `Fase2/Ejercicio2.2/factory.py` para obtener un template de `null_resource` que se pasa a `ResourcePrototype`.
3. Ejecuté `pytest` en la carpeta `Ejercicio3.3` y guardé la salida reducida en `pytest_results.txt`.


### Cómo ejecutar los tests

Desde la raíz del workspace, ejecutar:

```bash
pytest Actividad14-CC3S2/Fase3/Ejercicio3.3 -q
```

Para guardar la salida en un archivo (log resumido):

```bash
pytest Actividad14-CC3S2/Fase3/Ejercicio3.3 -q | tee Actividad14-CC3S2/Fase3/Ejercicio3.3/pytest_results.txt
```
