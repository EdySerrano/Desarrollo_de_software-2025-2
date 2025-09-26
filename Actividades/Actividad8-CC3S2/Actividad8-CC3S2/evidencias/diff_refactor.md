# Diff Refactor - Evidencias de Refactorización

## Fragmentos Antes/Después con Justificaciones

### 1. Mejora de Nombres - Test Parametrización

**ANTES:**
```python
@pytest.mark.parametrize("p,c,d,expected", [
    (10.0, 2, 0.1, 18.0),
    (5.0, 3, 0.2, 12.0),
])
def test_desc(p, c, d, expected):
    cart = Carrito()
    cart.agregar_producto(Producto("item", p), c)
    cart.aplicar_descuento(d)
    assert cart.calcular_total() == expected
```

**DESPUÉS:**
```python
@pytest.mark.parametrize("precio,cantidad,descuento,total_esperado", [
    (10.0, 2, 0.1, 18.0),  # 2*10 - 10% = 18
    (5.0, 3, 0.2, 12.0),   # 3*5 - 20% = 12  
])
def test_descuentos_parametrizados(precio, cantidad, descuento, total_esperado):
    cart = Carrito()
    producto = Producto("test_item", precio)
    cart.agregar_producto(producto, cantidad)
    cart.aplicar_descuento(descuento)
    assert cart.calcular_total() == total_esperado
```

**JUSTIFICACIÓN:**
- **Nombres descriptivos**: `precio` vs `p`, `cantidad` vs `c` mejoran legibilidad
- **Comentarios inline**: Documentan el cálculo esperado 
- **Consistencia**: Variables siguen convención snake_case consistente
- **Mantenibilidad**: Próximos desarrolladores entenderán parámetros inmediatamente

---

### 2. Eliminación de Duplicación - Factory Pattern

**ANTES:**
```python
def test_carrito_vacio():
    cart = Carrito()
    assert cart.calcular_total() == 0
    
def test_agregar_producto():
    cart = Carrito()  # Duplicado
    producto = Producto("test", 10.0)  # Duplicado
    cart.agregar_producto(producto, 2)
    assert cart.calcular_total() == 20.0
    
def test_remover_producto():
    cart = Carrito()  # Duplicado  
    producto = Producto("test", 10.0)  # Duplicado
    # ... más código duplicado
```

**DESPUÉS:**
```python
# factories.py
class ProductoFactory:
    @staticmethod
    def crear_basico(nombre="test_producto", precio=10.0):
        return Producto(nombre, precio)
        
    @staticmethod  
    def crear_con_faker():
        fake = Faker()
        return Producto(fake.word(), fake.pydecimal(left_digits=2, right_digits=2, positive=True))

# tests/test_shopping_cart.py
def test_carrito_vacio():
    cart = Carrito()
    assert cart.calcular_total() == 0
    
def test_agregar_producto():
    cart = Carrito()
    producto = ProductoFactory.crear_basico("laptop", 15.0)
    cart.agregar_producto(producto, 2)
    assert cart.calcular_total() == 30.0
```

**JUSTIFICACIÓN:**
- **DRY Principle**: Factory elimina duplicación de creación de objetos
- **Configurabilidad**: Factory permite variaciones controladas
- **Testabilidad**: Datos consistentes y faker para variabilidad
- **Separación de responsabilidades**: Factory maneja creación, tests verifican comportamiento

---

### 3. Separación de Responsabilidades - Mock Contracts

**ANTES:**
```python
def test_pago_directo():
    # Test acoplado a implementación real de pasarela
    cart = Carrito()
    cart.agregar_producto(Producto("item", 100), 1)
    # Llamada directa a sistema externo - frágil
    result = sistema_pago_real.procesar(cart.calcular_total())  
    assert result.success
```

**DESPUÉS:**
```python
@patch('src.carrito.PasarelaPago')
def test_contrato_pago_exitoso(mock_pasarela):
    # Arrange - Configuración del contrato
    mock_instance = mock_pasarela.return_value
    mock_instance.procesar_pago.return_value = {"exito": True, "id_transaccion": "12345"}
    
    cart = Carrito() 
    cart.agregar_producto(Producto("laptop", 100.0), 1)
    
    # Act - Ejercitar comportamiento
    resultado = cart.procesar_pago()
    
    # Assert - Verificar contrato
    mock_instance.procesar_pago.assert_called_once_with(100.0)
    assert resultado["exito"] is True
    assert "id_transaccion" in resultado
```

**JUSTIFICACIÓN:**
- **Aislamiento**: Tests no dependen de servicios externos
- **Velocidad**: Mocks son más rápidos que llamadas reales  
- **Predictibilidad**: Comportamiento controlado vs respuestas variables de red
- **Contrato testing**: Verificamos interacciones específicas, no implementación

---

### 4. Reducción de Acoplamiento - Dependency Injection

**ANTES:**
```python
class Carrito:
    def __init__(self):
        self.items = []
        self.pasarela = PasarelaPagoReal()  # Acoplamiento fuerte
        
    def procesar_pago(self):
        total = self.calcular_total()
        return self.pasarela.procesar(total)  # Dependencia hardcodeada
```

**DESPUÉS:**
```python
class Carrito:
    def __init__(self, pasarela_pago=None):
        self.items = []
        self.pasarela = pasarela_pago or PasarelaPagoReal()  # Inyección opcional
        
    def procesar_pago(self):
        total = self.calcular_total()
        return self.pasarela.procesar_pago(total)  # Interfaz consistente

# En tests:
def test_with_mock():
    mock_pasarela = Mock()
    cart = Carrito(pasarela_pago=mock_pasarela)  # Inyección para testing
    # Test con comportamiento controlado
```

**JUSTIFICACIÓN:**
- **Flexibilidad**: Permite diferentes implementaciones de pasarela
- **Testabilidad**: Fácil inyección de mocks para pruebas unitarias
- **Principio abierto/cerrado**: Extensible sin modificar código existente  
- **Inversión de dependencias**: Depende de abstracción, no implementación concreta

---

### 5. Mejora de Legibilidad - AAA Pattern Consistency

**ANTES:**
```python
def test_mixed_operations():
    cart = Carrito()
    cart.agregar_producto(Producto("a", 10), 2)
    assert cart.calcular_total() == 20
    cart.aplicar_descuento(0.1)
    cart.agregar_producto(Producto("b", 5), 1)  
    total = cart.calcular_total()
    assert total == 23.0  # ¿Cálculo unclear?
```

**DESPUÉS:**
```python
def test_descuento_con_productos_adicionales():
    # Arrange - Preparar estado inicial
    cart = Carrito()
    producto_inicial = Producto("laptop", 10.0)
    producto_adicional = Producto("mouse", 5.0)
    
    # Act - Ejecutar operaciones secuenciales  
    cart.agregar_producto(producto_inicial, 2)  # 2*10 = 20
    cart.aplicar_descuento(0.1)                 # 20 - 10% = 18
    cart.agregar_producto(producto_adicional, 1) # 18 + 5 = 23
    
    # Assert - Verificar resultado final
    total_final = cart.calcular_total()
    assert total_final == 23.0
```

**JUSTIFICACIÓN:**
- **Estructura clara**: AAA pattern separa fases del test
- **Documentación**: Comentarios explican cada paso del cálculo
- **Mantenibilidad**: Fácil seguimiento de la lógica de negocio
- **Debugging**: Cada fase claramente identificada para troubleshooting

---
