# Decisiones de Testing y Variables

## Contratos verificados por cada prueba 

### A1: Descuentos Parametrizados (`test_descuentos_parametrizados.py`)

**Contratos verificados:**
- **Cálculo correcto de subtotal**: `cantidad × precio = subtotal` 
- **Aplicación correcta de descuento**: `subtotal × (1 - descuento) = total`
- **Precisión decimal**: Resultados mantienen 2 decimales consistentes
- **Orden de operaciones**: Descuento se aplica al subtotal acumulado

**Qué garantiza del carrito:**
- El carrito calcula totales matemáticamente correctos
- Los descuentos porcentuales se aplican apropiadamente  
- No hay errores de redondeo en cálculos básicos
- Sistema es consistente en operaciones secuenciales

---

### A2: Idempotencia de Cantidades (`test_idempotencia_cantidades.py`)

**Contratos verificados:**
- **Agregar + Remover = Estado Original**: `add(n) -> remove(n) = ∅`
- **Operaciones reversibles**: Estado se puede restaurar completamente
- **Conservación de totales**: Suma total se mantiene consistente

**Qué garantiza del carrito:**
- Las operaciones son matemáticamente reversibles
- No hay efectos secundarios permanentes en operaciones compensatorias
- El estado del carrito es predecible y consistente
- Sistema robusto para correcciones de usuarios

---

### A3: Precios Frontera (`test_precios_frontera.py`)

**Contratos verificados:**
- **Precios válidos procesados**: `precio > 0` acepta correctamente
- **Precios inválidos rechazados**: `precio ≤ 0` (contrato indefinido - XFAIL)
- **Precisión en casos límite**: Decimales pequeños manejados correctamente  
- **Comportamiento consistente**: Misma lógica independiente del valor

**Qué garantiza del carrito:**
- Sistema maneja precios positivos correctamente
- Documentación de casos edge no definidos (precio cero/negativo)
- Comportamiento predecible para rangos válidos de entrada
- Identificación de gaps en especificaciones de negocio

---

### A4: Redondeo Acumulado (`test_redondeo_acumulado.py`)

**Contratos verificados:**
- **Consistencia de redondeo**: Mismo resultado con diferentes enfoques
- **Precisión financiera**: Diferencias < 0.01 (tolerancia de centavos)
- **Robustez numérica**: Manejo correcto de punto flotante
- **Coherencia del SUT**: Comportamiento uniforme entre clases

**Qué garantiza del carrito:**
- Cálculos financieros son confiables para transacciones reales
- No hay discrepancias entre diferentes métodos de cálculo
- Sistema cumple estándares de precisión monetaria
- Robustez ante variaciones de entrada con decimales complejos

---

### B1-B3: RGR Precision (`test_rgr_precision_*.py`)

**Contratos verificados:**
- **RED**: `test_total_precision_decimal` - Documenta limitación float (XFAIL)
- **GREEN**: Implementación actual pasa tests de precisión básica
- **REFACTOR**: Tests mantienen comportamiento tras refactorización

**Qué garantiza del carrito:**
- Documentación ejecutable de limitaciones conocidas (precisión binaria)
- Especificación de comportamiento esperado vs actual
- Tests como especificación para futuras mejoras
- Ciclo de desarrollo disciplinado (RGR)

---

### C1: Contratos de Pasarela de Pago (`test_pasarela_pago_contratos.py`)

**Contratos verificados:**
- **Interfaz de pago consistente**: Mock verifica llamadas correctas
- **Manejo de respuesta exitosa**: Procesamiento correcto de confirmaciones
- **Manejo de fallos de pago**: Propagación apropiada de errores
- **Aislamiento de servicios externos**: Tests no dependen de red

**Qué garantiza del sistema de pagos:**
- Integración robusta con pasarelas externas
- Contratos de API bien definidos y verificados
- Resiliencia ante fallos de servicios externos  
- Testabilidad sin dependencias de infraestructura

---

### C2: Marcadores CI/CD (`test_markers.py`)

**Contratos verificados:**
- **Smoke tests**: Funcionalidad crítica opera correctamente
- **Regression tests**: Cambios no rompen comportamiento existente
- **Categorización para pipeline**: Tests organizados por propósito
- **Execution efficiency**: Subconjuntos ejecutables independientemente

**Qué garantiza del pipeline:**
- CI/CD puede ejecutar subconjuntos optimizados por contexto
- Tests críticos se ejecutan en cada commit (smoke)
- Tests exhaustivos se ejecutan en releases (regression)
- Feedback rápido para desarrolladores

---

### C4: MREs (`test_mre_precision.py`)

**Contratos verificados:**
- **Reproducibilidad**: Casos mínimos documentan defectos específicos
- **Aislamiento**: Cada MRE verifica un problema específico
- **Comunicación**: Síntomas y expectativas claramente definidos

**Qué garantiza del proceso:**
- Defectos están documentados de manera ejecutable  
- Casos de prueba mínimos para debugging eficiente
- Regresión prevention cuando defectos se corrijan
- Comunicación clara entre QA y desarrollo

---

### D1: Estabilidad con Semillas (`test_estabilidad_semillas.py`)

**Contratos verificados:**
- **Determinismo**: Semilla fija -> mismos datos -> mismos resultados
- **Reproducibilidad**: Tests generan outputs idénticos cross-run
- **Control de variabilidad**: Randomness controlado vs caótico
- **Debugging facilitado**: Comportamiento predecible para troubleshooting

**Qué garantiza del testing:**
- Tests complejos son reproducibles y debuggable
- Variabilidad controlada permite explorar edge cases
- CI/CD resultados consistentes
- Effective chaos engineering con control

---

### D2: Invariantes de Inventario (`test_invariantes_inventario.py`)

**Contratos verificados:**
- **Reversibilidad**: `agregar(n) → remover(n) = estado_inicial`
- **Consistencia**: Operaciones preservan integridad del estado
- **Acumulación**: Múltiples operaciones mantienen coherencia
- **Aislamiento**: Productos independientes no se afectan mutuamente

**Qué garantiza del inventario:**
- Invariantes fundamentales de negocio se mantienen
- Operaciones no introducen inconsistencias de estado
- Sistema es matemáticamente correcto
- Robustez ante secuencias complejas de operaciones

---

### D3: Contratos de Mensajes (`test_mensajes_error.py`)

**Contratos verificados:**
- **Mensajes informativos**: Errores incluyen contexto suficiente
- **Especificidad**: Valores exactos en mensajes (XFAIL - mejora futura)
- **Contexto accionable**: Guías para corrección (XFAIL - UX improvement)
- **Consistencia**: Formato uniforme de mensajes de error

**Qué garantiza del UX:**
- Errores proporcionan información útil para usuarios
- Debugging es más eficiente con contexto específico
- Documentación de mejoras deseadas en experiencia de usuario
- Contratos ejecutables para evolución del sistema

---

## Variables y Efectos Observables

### Variables de Configuración Identificadas

#### `DISCOUNT_RATE` (Implícito en parametrización)
- **Ubicación**: `test_descuentos_parametrizados.py` 
- **Valores testados**: `0.1, 0.2, 0.15` (10%, 20%, 15%)
- **Efecto observable**: Modificación directa del total final calculado
- **Fórmula**: `total_final = subtotal × (1 - DISCOUNT_RATE)`
- **Comportamiento**: Lineal, inversamente proporcional al total

#### `TAX_RATE` (Potencial - no implementado actualmente)
- **Status**: No detectado en SUT actual
- **Efecto esperado**: `total_con_impuesto = subtotal × (1 + TAX_RATE)`  
- **Testing**: Sería parametrizable similar a descuentos
- **Consideración**: Futura expansión del sistema

#### `PRECISION_DECIMALS` (Implícito en redondeo)
- **Ubicación**: Observado en `test_redondeo_acumulado.py`
- **Valor actual**: `2 decimales` (estándar monetario)
- **Efecto observable**: Determina precisión de cálculos financieros
- **Validación**: Diferencias < `10^-2` consideradas insignificantes

#### `PAYMENT_TIMEOUT` (Mock configuration)
- **Ubicación**: `test_pasarela_pago_contratos.py`
- **Efecto observable**: Determina comportamiento de timeout en pagos
- **Testing**: Verificado via mock configurations
- **Impacto**: Critical para UX en transacciones

---

## Casos Borde Considerados y Ubicación

### Casos Borde Matemáticos

#### **Precisión de Punto Flotante**
- **Dónde**: `test_redondeo_acumulado.py` 
- **Casos**: `0.1×3`, `0.125×4`, `0.335×3 + 0.225×4`
- **Validación**: Diferencias < `10^-15` (precisión de máquina)
- **Resultado**: Sistema robusto ante errores de representación binaria

#### **Operaciones Reversibles**  
- **Dónde**: `test_idempotencia_cantidades.py`
- **Casos**: `add(n) -> remove(n)`, secuencias largas de operaciones
- **Validación**: Estado final == estado inicial
- **Resultado**: Matemáticamente correcto, sin drift acumulativo

#### **Valores Límite de Precios**
- **Dónde**: `test_precios_frontera.py`
- **Casos**: `precio = 0.01` (mínimo), `precio = 0` (XFAIL), `precio < 0` (XFAIL)  
- **Validación**: Comportamiento definido vs casos edge indefinidos
- **Resultado**: Gaps identificados en especificación de negocio

### Casos Borde de Integración

#### **Fallos de Servicios Externos**
- **Dónde**: `test_pasarela_pago_contratos.py`
- **Casos**: Network timeout, invalid response, service unavailable
- **Validación**: Excepciones apropiadas, fallback behavior
- **Resultado**: Sistema resiliente ante fallos de infraestructura

#### **Datos Inválidos de Usuario**
- **Dónde**: `test_mensajes_error.py`  
- **Casos**: Cantidades negativas, productos inexistentes, descuentos inválidos
- **Validación**: Mensajes informativos vs mensajes genéricos (XFAIL)
- **Resultado**: UX gaps identificados para mejora

---
