# Resumen de Cobertura - Análisis y Plan de Mejora

## Reporte de `make cov` - Cobertura Actual

```
================================ tests coverage ================================
_______________ coverage: platform linux, python 3.10.12-final-0 _______________

Name                                      Stmts   Miss  Cover   Missing
-----------------------------------------------------------------------
src/__init__.py                               0      0   100%
src/carrito.py                               55      4    93%   9, 21, 64, 97
src/factories.py                              7      0   100%
src/shopping_cart.py                         29      2    93%   9, 27
tests/__init__.py                             0      0   100%
tests/test_descuentos_parametrizados.py       9      0   100%
tests/test_estabilidad_semillas.py           85      1    99%   87
tests/test_idempotencia_cantidades.py        14      0   100%
tests/test_invariantes_inventario.py         74      0   100%
tests/test_markers.py                        61      0   100%
tests/test_mensajes_error.py                 86      2    98%   51, 84
tests/test_mre_precision.py                  27      0   100%
tests/test_pasarela_pago_contratos.py        67      0   100%
tests/test_precios_frontera.py               14      0   100%
tests/test_redondeo_acumulado.py             45      0   100%
tests/test_refactor_suites.py                68      0   100%
tests/test_rgr_precision_rojo.py             16      0   100%
tests/test_rgr_precision_verde.py            16     10    38%   8-18, 23-32
tests/test_shopping_cart.py                  47      0   100%
-----------------------------------------------------------------------
TOTAL                                       720     19    97%
============= 59 passed, 2 skipped, 6 xfailed, 2 xpassed in 0.90s ==============
```

## Plan Breve para Subir Cobertura

### Fase 1: Correcciones Críticas (Prioridad Alta)

1. **Investigar línea 64 en carrito.py**
   ```bash
   # Crear test específico para el bug detectado:
   pytest tests/test_mensajes_error.py::test_mensaje_error_cantidad_negativa -v
   ```
   
2. **Test para actualizar_cantidad con valores negativos**
   ```python
   def test_actualizar_cantidad_negativa():
       # Debería cubrir línea 64 y validar manejo de error
   ```

### Fase 2: Paths de Error (Prioridad Media)  

3. **Tests para líneas 9 y 97 en carrito.py**
   ```python
   def test_carrito_inicializacion_error():
       # Cubrir excepciones en constructor
       
   def test_carrito_limpieza_recursos():  
       # Cubrir cleanup paths
   ```

4. **Tests para líneas 9 y 27 en shopping_cart.py**
   ```python
   def test_shopping_cart_paths_alternativos():
       # Cubrir inicialización y métodos auxiliares
   ```

### Fase 3: Optimización (Prioridad Baja)

5. **Activar tests skipped en test_rgr_precision_verde.py**
   - Después de completar ciclo RGR real
   - Remover markers `@pytest.mark.skip`
   - Validar que pasen correctamente

### Proyecciones de Mejora

| Fase | Líneas Target | Cobertura Esperada | Esfuerzo |
|------|---------------|-------------------|----------|
| **Actual** | - | 97% | - |
| **Fase 1** | 2-3 líneas | 97.5% | 2-3 tests |
| **Fase 2** | 4-5 líneas | 98.2% | 4-5 tests |  
| **Fase 3** | 10 líneas | 99.5% | Activar existentes |
| **Meta Final** | 19 líneas | **99.5%** | ~7 tests nuevos |

## Ramas/Módulos No Cubiertos por Categoría

### Core Business Logic (src/)
- **93% cubierto** - Excelente para lógica principal  
- **Target**: 98% - Agregar tests para edge cases

### Test Infrastructure (tests/)
- **95% cubierto** - Muy buena cobertura de infraestructura
- **Target**: 100% - Activar tests condicionales

### Manejo de Errores
- **Parcialmente cubierto** - Algunos paths de error faltantes
- **Target**: 100% - Crítico para robustez

### Validaciones de Entrada  
- **Parcialmente cubierto** - Validaciones defensivas faltantes
- **Target**: 95% - Importante para seguridad


