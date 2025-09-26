# Análisis del Ejercicio A1: Descuentos Parametrizados

## A1. Descuentos parametrizados

### Descripción
Se creó el archivo `tests/test_descuentos_parametrizados.py` con casos de prueba parametrizados que verifican el cálculo de totales con diferentes descuentos aplicados sobre productos con diversos precios y cantidades.

### Implementación
- Se utilizó el patrón AAA (Arrange, Act, Assert) comentado en cada prueba
- Se implementaron 6 casos de prueba parametrizados con `@pytest.mark.pEstado: **4 MREs creados y documentados**


## A2. Idempotencia de actualización de cantidades

### Descripción
Se creó el archivo `tests/test_idempotencia_cantidades.py` para verificar que establecer varias veces la misma cantidad no cambia el total ni el número de ítems en el carrito, cumpliendo así con el principio de idempotencia.

### Implementación
- Se utilizó el patrón AAA (Arrange, Act, Assert) comentado en la prueba
- Se adaptó la API existente usando `agregar_producto`, `actualizar_cantidad`, `calcular_total` y `contar_items`
- Se realizó la operación de actualización 5 veces consecutivas para verificar la idempotencia
- Se verificaron tanto el total como el número de ítems antes y después de las operaciones

### Casos verificados
- **Producto**: "x" con precio 3.25
- **Cantidad inicial**: 2 unidades
- **Operación**: Actualizar cantidad a 2 (5 veces consecutivas)
- **Verificaciones**: Total constante (6.50) y número de ítems constante (2)

### Resultados
- La prueba pasa exitosamente (1/1)
- Se comprueba que `actualizar_cantidad` es idempotente
- Total de pruebas en el proyecto: 13/13 pasan
- La cobertura aumentó del 60% al 68%

## A3. Fronteras de precio y valores inválidos

### Descripción
Se creó el archivo `tests/test_precios_frontera.py` para cubrir casos extremos de precios, incluyendo valores frontera y precios inválidos, utilizando `xfail` para casos donde el comportamiento no está definido por el SUT.

### Implementación
- Se utilizó el patrón AAA (Arrange, Act, Assert) comentado en las pruebas
- Se implementaron pruebas parametrizadas para valores frontera usando `@pytest.mark.parametrize`
- Se usó `@pytest.mark.xfail` para precios inválidos donde el contrato no está definido
- Se adaptó la API existente usando `agregar_producto` y `calcular_total`

### Resultados
- **Pruebas de frontera**: 4/4 pasan
- **Pruebas inválidas**: 2/2 XPASS (comportamiento inesperado)
- **Descubrimiento**: El SUT acepta precios 0 y negativos sin lanzar excepciones
- **Total de pruebas**: 17 pasan, 2 XPASS (19 totales)
- **Cobertura**: Se mantiene en 68%

## A4. Redondeos acumulados vs. final

### Descripción
Se creó el archivo `tests/test_redondeo_acumulado.py` para analizar las diferencias entre redondear el total de cada ítem individualmente versus redondear la suma final, documentando casos donde estos enfoques pueden diferir.

### Implementación
- Se utilizó el patrón AAA (Arrange, Act, Assert) comentado en las pruebas
- Se crearon múltiples casos para explorar diferentes escenarios de redondeo
- Se calculan tanto la suma exacta como los redondeos por ítem y final
- Se documentan las diferencias numéricas para análisis

### Mini-tabla: Suma por ítem / Redondeo final / Diferencia

| Caso | Suma Exacta | Redondeo por Ítem | Redondeo Final | Diferencia |
|------|-------------|-------------------|----------------|------------|
| A: 0.3333×3 + 0.6667×3 | 3.0000 | 3.00 | 3.00 | 0.00 |
| B: 0.125×4 + 0.124×4 | 0.996 | 1.00 | 1.00 | 0.00 |
| C: 0.335×3 + 0.225×4 | 1.905 | 1.91 | 1.91 | ~0.00* |
| D: 1.225×2 + 0.375×4 | 3.950 | 3.95 | 3.95 | 0.00 |

*Diferencia menor a precisión de punto flotante


### Resultados
- **Pruebas de redondeo**: 3/3 pasan
- **Total de pruebas**: 20 pasan, 2 XPASS (22 totales)
- **Cobertura**: Aumentó del 68% al 69%
- **Comportamiento del SUT**: Consistente en manejo de redondeos

## B1. RGR - Rojo (falla esperada) - precisión financiera

### Descripción
Se creó el archivo `tests/test_rgr_precision_rojo.py` con pruebas marcadas como `@pytest.mark.xfail` para demostrar el problema clásico de precisión binaria en operaciones financieras con números de punto flotante.

### Implementación
- Se utilizaron dos pruebas con `@pytest.mark.xfail` para documentar fallas esperadas
- Primera prueba: problema de precisión en cálculo directo sin redondeo
- Segunda prueba: demostración del caso clásico 0.1 + 0.2 != 0.3
- Se usa `ShoppingCart` según las pistas del ejercicio

### Resultados
- **Pruebas con XFAIL**: 2/2 fallan como se esperada
- **Total de pruebas**: 20 pasan, 2 XFAIL, 2 XPASS (24 totales)
- **Cobertura**: Se mantiene en 69%
- **Demostración exitosa**: Se documenta el problema de precisión binaria

## B2. RGR - Verde (exclusión documentada)

### Descripción
Se creó el archivo `tests/test_rgr_precision_verde.py` convirtiendo las pruebas del ejercicio B1 de `@pytest.mark.xfail` a `@pytest.mark.skip`, representando la fase "Verde" del ciclo RGR donde se decide excluir temporalmente la corrección del problema para mantener la estabilidad del pipeline.

### Implementación
- Se convirtieron 2 pruebas de `xfail` a `skip` con razones explícitas y documentadas
- Primera prueba: "Contrato: precisión binaria no se corrige en esta versión"
- Segunda prueba: "Problema de precisión conocido - no implementado en esta versión"
- Mismo setup que el ejercicio B1 pero con exclusión intencional

**Razones para la exclusión:**
1. **Estabilidad del pipeline**: Evitar fallas en CI/CD por problemas conocidos pero no críticos
2. **Priorización de features**: La precisión decimal no es crítica para esta versión del producto
3. **Complejidad vs beneficio**: Implementar `decimal.Decimal` requiere refactoring extensivo

### Resultados
- **Pruebas skipped**: 2/2 se omiten correctamente
- **Total de pruebas**: 20 pasan, 2 SKIPPED, 2 XFAIL, 2 XPASS (26 totales)
- **Cobertura**: Se mantiene en 69%
- **Pipeline verde**: Sin fallas por problemas de precisión conocidos

## B3. RGR - Refactor de suites

### Descripción
Se creó el archivo `tests/test_refactor_suites.py` reorganizando casos de prueba en dos clases especializadas por dominio: `TestPrecisionMonetaria` y `TestPasarelaPagoContratos`, mejorando la legibilidad y mantenibilidad sin duplicar lógica.

### Implementación de la reorganización
Se aplicaron principios de Single Responsibility Principle (SRP) para agrupar pruebas relacionadas:

**Clase `TestPrecisionMonetaria`:** (4 pruebas)
- `test_suma_pequenas_cantidades`: Verificación de sumas de decimales pequeños
- `test_precision_con_decimales`: Prueba de precisión con valores decimales diversos
- `test_redondeo_consistente`: Validación del redondeo a 2 decimales
- `test_aplicacion_descuento_precision`: Precisión en cálculo de descuentos

**Clase `TestPasarelaPagoContratos`:** (5 pruebas)
- `test_pago_exitoso`: Flujo exitoso de procesamiento de pago
- `test_pago_fallido`: Manejo de pagos rechazados
- `test_excepcion_sin_pasarela`: Validación de excepción por falta de pasarela
- `test_excepcion_en_procesamiento`: Manejo de excepciones durante el procesamiento
- `test_monto_con_descuento`: Integración de descuentos con procesamiento de pago

### Resultados
- **Pruebas refactorizadas**: 9/9 pasan correctamente
- **Total de pruebas**: 29 pasan, 2 SKIPPED, 2 XFAIL, 2 XPASS (35 totales)
- **Cobertura mejorada**: Del 69% al 70% (+1%)
- **Refactor exitoso**: Mejor organización sin duplicación de lógica

## C1. Contratos de pasarela de pago con mock

### Descripción
Se creó el archivo `tests/test_pasarela_pago_contratos.py` para validar exhaustivamente los contratos de interacción con pasarelas de pago externas, cubriendo escenarios de éxito, fallos transitorios y rechazos definitivos usando mocks.

### Implementación
Se desarrollaron 7 pruebas que cubren todos los escenarios críticos de procesamiento de pagos:
- **Éxito**: Pago procesado correctamente
- **Timeout**: Excepción transitoria sin reintento automático
- **Rechazo**: Respuesta definitiva negativa
- **Errores de red**: Excepciones de conectividad
- **Errores de validación**: Datos inválidos
- **Sin pasarela**: Validación de configuración requerida
- **Monto cero**: Caso edge de transacciones gratuitas

### Tabla: Evento -> Expectativa

| Evento | Mock Configuración | Expectativa del SUT | Verificación |
|--------|-------------------|-------------------|--------------|
| **Pago exitoso** | `process_payment.return_value = True` | Retorna `True` | Una llamada al mock |
| **Timeout transitorio** | `process_payment.side_effect = TimeoutError` | Lanza `TimeoutError` | Sin reintentos automáticos (1 llamada) |
| **Rechazo definitivo** | `process_payment.return_value = False` | Retorna `False` | Una llamada al mock |
| **Error de red** | `process_payment.side_effect = ConnectionError` | Lanza `ConnectionError` | Sin reintentos automáticos (1 llamada) |
| **Tarjeta inválida** | `process_payment.side_effect = ValueError` | Lanza `ValueError` | Sin reintentos automáticos (1 llamada) |
| **Sin pasarela** | `ShoppingCart()` sin gateway | Lanza `ValueError` | Error antes de llamar al mock |
| **Monto cero** | `process_payment.return_value = True` | Retorna `True` con monto 0.0 | Una llamada con parámetro 0.0 |

### Resultados
- **Contratos validados**: 7/7 escenarios cubiertos
- **Total de pruebas**: 36 pasan, 2 SKIPPED, 2 XFAIL, 2 XPASS (42 totales)
- **Cobertura mantenida**: 93% en shopping_cart.py, 70% total
- **Mock contracts**: Comportamiento de pasarelas externas documentado


## C2: Marcadores de Pruebas para CI/CD

### Implementación

Creamos marcadores personalizados en `tests/test_markers.py`:

- **@pytest.mark.smoke**: 3 pruebas críticas para validación rápida
- **@pytest.mark.regression**: 5 pruebas exhaustivas para estabilidad completa


## C3: Umbral de Cobertura como Quality Gate

### Implementación del Quality Gate

Se ejecutó el comando con umbral de cobertura del 90%:
```bash
pytest --cov=src --cov-report=term-missing --cov-fail-under=90
```

### Resultado del Quality Gate

**FALLA**: La cobertura total (70%) no alcanza el umbral del 90%


## C4: MREs (Minimal Reproducible Examples) para Defectos

### Implementación

Creamos `tests/test_mre_precision.py` con 4 MREs que documentan defectos identificados en el proyecto:

### MRE 1: Error de Precisión Binaria

**Síntoma**: Posibles errores de precisión en aritmética de punto flotante
**Pasos**: 1) Crear carrito, 2) Agregar items con decimales, 3) Calcular total
**Expectativa**: Total exacto de 0.3

### MRE 2: Acumulación de Errores

**Síntoma**: Acumulación de errores de precisión con múltiples operaciones
**Pasos**: 1) Agregar 10 items de 0.1, 2) Calcular total acumulado
**Expectativa**: Total de 1.00 exacto

### MRE 3: Contrato Indefinido para Precio Cero

**Síntoma**: Comportamiento no especificado para precios cero/negativos
**Pasos**: 1) Crear producto con precio 0, 2) Agregarlo al carrito, 3) Calcular
**Expectativa**: ¿Debería permitirse? Contrato no define comportamiento

### MRE 4: Diferencias entre Implementaciones

**Síntoma**: Posibles diferencias en manejo de precisión entre clases
**Pasos**: 1) Mismo cálculo en ambas clases, 2) Comparar resultados
**Expectativa**: Ambas implementaciones deberían ser consistentes

### Análisis de Defectos

#### Defectos Identificados en xfail/skip:

1. **test_total_precision_decimal** (xfail)
   - **Ubicación**: `tests/test_rgr_precision_rojo.py`
   - **Síntoma**: "Float binario puede introducir error en dinero"
   - **MRE asociado**: `test_mre_precision_float_binary`

2. **test_precision_binaria_directa** (xfail)  
   - **Ubicación**: `tests/test_rgr_precision_rojo.py`
   - **Síntoma**: "Demostración directa del problema de precisión binaria"
   - **MRE asociado**: `test_mre_precision_accumulated`

3. **test_precios_invalidos** (xfail)
   - **Ubicación**: `tests/test_precios_frontera.py` 
   - **Síntoma**: "Contrato no definido para precio=0 o negativo"
   - **MRE asociado**: `test_mre_precio_cero_indefinido`





## D2: Invariantes de Inventario

### Implementación

Creamos `tests/test_invariantes_inventario.py` con 5 tests que validan invariantes fundamentales del carrito de compras para prevenir regresiones en la lógica de negocio.

### Invariantes Validados

#### 1. Invariante Principal: Reversibilidad Completa

**Propósito**: Garantiza que agregar N y luego remover N vuelve al estado inicial vacío

#### 2. Invariante de Consistencia Parcial

**Propósito**: Las operaciones parciales mantienen consistencia matemática

#### 3. Invariante de Acumulación Sin Duplicación

**Propósito**: Agregar el mismo producto acumula cantidades, no crea duplicados

#### 4. Invariante de Aislamiento entre Productos

**Propósito**: Las operaciones en un producto no afectan otros productos

#### 5. Invariante de Ciclo Completo

**Propósito**: Un ciclo completo de operaciones vuelve al estado original

### Implementación

Creamos `tests/test_estabilidad_semillas.py` con 4 tests que demuestran control determinístico de datos aleatorios mediante semillas fijas.

### Tests de Estabilidad Implementados

#### 1. Test Básico de Estabilidad

**Verificación**: Mismo producto, precio y total en ambas ejecuciones

#### 2. Test Múltiples Productos Aleatorios  

**Verificación**: Mismo número de items y total con semilla 456

#### 3. Test Inestabilidad Sin Semillas

**Contraste**: Sin semillas, productos son diferentes (como esperado)

#### 4. Test Estabilidad con Descuentos

**Verificación**: Mismo descuento y total final con semilla 789

### Resultados
- Todas las pruebas pasaron exitosamente (6/6)
- La cobertura actual es del 60% que es inferior al 90% requerido
- Se generaron correctamente los archivos `out/junit.xml` y `out/coverage.txt`


## D3: Contrato de Mensajes de Error

### Implementación

Creamos `tests/test_mensajes_error.py` con 6 tests que validan si los mensajes de excepción contienen contexto accionable para usuarios y desarrolladores.

### Análisis de Comportamiento Actual vs Deseado

#### Mensajes Actuales del Sistema (Capturados en Tests)

1. **Cantidad Excesiva en Remoción**:
   ```
   Mensaje actual: "Cantidad a remover es mayor que la cantidad en el carrito"
   Contexto faltante: No especifica cantidad solicitada ni disponible
   ```

2. **Producto Inexistente**:
   ```
   Mensaje actual: "Producto no encontrado en el carrito"  
   Contexto faltante: No incluye nombre específico del producto
   ```

3. **Descuento Inválido**:
   ```
   Mensaje actual: "El porcentaje debe estar entre 0 y 100"
   Contexto faltante: No incluye el valor específico inválido
   ```

### Estado del Sistema Actual

- **2 tests PASAN**: Funciones que funcionan correctamente
- **4 tests XFAIL**: Contratos deseados documentados para futuras mejoras  
- **Bug identificado**: `actualizar_cantidad()` impide algunas validaciones
- **Gap de UX**: Mensajes genéricos requieren mejora sistemática

Los contratos XFAIL sirven como especificación ejecutable de los mensajes de error mejorados que beneficiarían significativamente la experiencia del usuario y la capacidad de mantenimiento del sistema.

Estado: **Contratos de mensajes documentados con 4 XFAIL para mejoras de UX**
