# Actividad 9 - CC3S2: Testing en Python con Pytest

[![Python Version](https://img.shields.io/badge/Python-3.12.3-blue.svg)](https://python.org)
[![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen.svg)](https://github.com/nedbat/coveragepy)
[![Tests](https://img.shields.io/badge/Tests-46%20passed-brightgreen.svg)](https://docs.pytest.org/)

Este proyecto implementa una serie de ejercicios prácticos sobre testing en Python, cubriendo conceptos fundamentales como aserciones, fixtures, coverage, factories/fakes, mocking de objetos y desarrollo dirigido por pruebas (TDD).

## Configuración del Entorno

### Requisitos
- **Python**: 3.12.3 (recomendado) o superior
- **Sistema Operativo**: Linux/macOS/Windows
- **Git**: Para clonar el repositorio

### Instalación

1. **Clonar el repositorio:**
```bash
git clone <repository-url>
cd /../Actividad9-CC3S2
```

2. **Crear entorno virtual:**
```bash
make venv
# O manualmente: python3 -m venv .venv
```

3. **Instalar dependencias:**
```bash
make deps
# O manualmente: .venv/bin/pip install -r requirements.txt
```

### Dependencias Principales
```
pytest==8.3.3
pytest-cov==5.0.0
faker==37.11.0
pytest-random-order==1.2.0
flask==2.1.2
flask-sqlalchemy==2.5.1
factory-boy==3.3.0
requests==2.31.0
```

## Ejecución de Pruebas

### Comandos Disponibles

```bash
# Ejecutar todas las pruebas
make test_all

# Ejecutar pruebas con cobertura (módulo coverage_pruebas)
make cov

# Generar reporte HTML de cobertura detallado
make coverage_individual

# Limpiar archivos temporales
make clean
```

### Ejecución Manual por Módulo

```bash
# Aserciones básicas
cd soluciones/aserciones_pruebas && ../../.venv/bin/pytest -v

# Pruebas con pytest
cd soluciones/pruebas_pytest && ../../.venv/bin/pytest -v

# Fixtures
cd soluciones/pruebas_fixtures && ../../.venv/bin/pytest -v

# Coverage
cd soluciones/coverage_pruebas && ../../.venv/bin/pytest --cov=models --cov-report=term-missing

# Factories y Fakes
cd soluciones/factories_fakes && ../../.venv/bin/pytest -v

# Mocking de objetos
cd soluciones/mocking_objetos && ../../.venv/bin/pytest -v

# Practica TDD
cd soluciones/practica_tdd && ../../.venv/bin/pytest -v
```

## Estructura del Proyecto

```
Actividad9-CC3S2/
├── Makefile                    # Automatizacion de tareas
├── README.md                   # Este archivo
├── requirements.txt            # Dependencias Python
├── evidencias/                 # Resultados y capturas
│   ├── cobertura_resumen.txt   # Resumen de cobertura
│   ├── sesion_pytest.txt       # Log completo de ejecución
│   └── capturas/               # Capturas de pantalla
└── soluciones/                 # Implementaciones por módulo
    ├── aserciones_pruebas/     # Ejercicio 1: Stack y aserciones
    ├── pruebas_pytest/         # Ejercicio 2: Triángulos con pytest
    ├── pruebas_fixtures/       # Ejercicio 3: Fixtures con Account
    ├── coverage_pruebas/       # Ejercicio 4: Análisis de cobertura
    ├── factories_fakes/        # Ejercicio 5: Factory Boy
    ├── mocking_objetos/        # Ejercicio 6: Mocking de APIs
    └── practica_tdd/           # Ejercicio 7: TDD con Flask
```

## Tecnicas de Testing Implementadas

### 1. **Aserciones (aserciones_pruebas)**
- **Implementación**: Clase `Stack` con operaciones básicas
- **Aserciones utilizadas**: 
  - `assert stack.is_empty()` - Verificar estado vacío
  - `assert stack.size() == expected` - Verificar tamaño
  - `pytest.raises(IndexError)` - Verificar excepciones esperadas
- **Cobertura**: 4 pruebas, funcionalidad completa de pila

### 2. **Fixtures (pruebas_fixtures)**
- **Implementación**: Modelo `Account` con SQLAlchemy
- **Fixtures creados**:
  - `@pytest.fixture` para setup de base de datos
  - Fixture de datos JSON para casos de prueba
  - Setup/teardown automático con `autouse=True`
- **Ventajas**: Reutilización de código, estado consistente entre pruebas

### 3. **Coverage Analysis (coverage_pruebas)**
- **Resultado**: **100% de cobertura** en el paquete `models`
- **Metricas**:
  - 59 statements totales, 0 no cubiertos
  - 14 branches totales, 0 parcialmente cubiertos
  - 12 pruebas ejecutadas exitosamente

### 4. **Factories y Fakes (factories_fakes)**
- **Factory Boy**: Generación automatizada de datos de prueba
- **Implementación**:
  ```python
  class AccountFactory(factory.Factory):
      name = factory.Faker('name')
      email = factory.Faker('email')
      phone_number = factory.Faker('phone_number')
  ```
- **Ventajas**: Datos realistas, tests más robustos, menos setup manual

### 5. **Mocking de Objetos (mocking_objetos)**
- **API simulada**: IMDb API para búsquedas de películas
- **Patrones implementados**:
  - `@patch('models.imdb.requests.get')` - Interceptar llamadas HTTP
  - Mock objects con `status_code` y `json()` configurables
  - Fixtures JSON para respuestas predefinidas
- **Casos cubiertos**:
  - Busquedas exitosas y fallidas
  - Manejo de API keys invalidas
  - Diferentes codigos de estado HTTP (200, 404, 500)

### 6. **Test-Driven Development (practica_tdd)**
- **Ciclo TDD implementado**: Red -> Green -> Refactor
- **API Flask** con endpoints para contadores:
  ```
  POST   /counters/<name>           # Crear contador
  GET    /counters/<name>           # Leer contador  
  PUT    /counters/<name>           # Incrementar contador
  DELETE /counters/<name>           # Eliminar contador
  GET    /counters                  # Listar todos
  PUT    /counters/<name>/increment # Incrementar (ruta dedicada)
  PUT    /counters/<name>/set       # Establecer valor específico
  PUT    /counters/<name>/reset     # Resetear a 0
  ```

#### Ejemplo del Ciclo TDD:

**Red - Escribir prueba que falle:**
```python
def test_increment_counter(client):
    client.post("/counters/my_counter")
    response = client.put("/counters/my_counter/increment")
    assert response.status_code == HTTPStatus.OK
    assert response.get_json()["my_counter"] == 1
```

**Green - Implementar funcionalidad mínima:**
```python
@app.route("/counters/<name>/increment", methods=["PUT"])
@require_counter
def increment_counter(name):
    return change_counter(name, +1), status.HTTP_200_OK
```

**Refactor - Mejorar diseño:**
```python
def change_counter(name, delta):
    """Función auxiliar que centraliza la lógica de modificación"""
    COUNTERS[name] += delta
    return {name: COUNTERS[name]}

def require_counter(func):
    """Decorador que verifica existencia del contador"""
    @wraps(func)
    def wrapper(name, *args, **kwargs):
        if name not in COUNTERS:
            return {"message": f"Counter '{name}' not found"}, 404
        return func(name, *args, **kwargs)
    return wrapper
```

## Resultados

- **Total de pruebas**: 46 pruebas
- **Tasa de éxito**: 100% (46/46 passed)
- **Cobertura máxima**: 100% en módulo coverage_pruebas
- **Tiempo de ejecución**: ~2.8 segundos total

### Desglose por Módulo
| Módulo | Pruebas | Estado | Cobertura |
|--------|---------|---------|-----------|
| aserciones_pruebas | 4 | PASS | N/A |
| pruebas_pytest | 11 | PASS | 100% |
| pruebas_fixtures | 2 | PASS | N/A |
| coverage_pruebas | 12 | PASS | 100% |
| factories_fakes | 8 | PASS | N/A | 
| mocking_objetos | 7 | PASS | 100% |
| practica_tdd | 9 | PASS | N/A |
