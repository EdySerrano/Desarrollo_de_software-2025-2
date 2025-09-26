"""
MREs (Minimal Reproducible Examples) para defectos identificados
"""
import pytest
from src.shopping_cart import ShoppingCart
from src.carrito import Carrito, ItemCarrito, Producto

def test_mre_precision_float_binary():
    """MRE: Error de precisión binaria en cálculos monetarios"""
    c = ShoppingCart()
    c.add_item("item1", 1, 0.1)  # Item diferente
    c.add_item("item2", 1, 0.2)  # Item diferente  
    # Expectativa: 0.1 + 0.2 = 0.3
    # Realidad: 0.30000000000000004 debido a precisión binaria
    raw_total = c.calculate_total()
    print(f"Total crudo: {raw_total}, redondeado: {round(raw_total, 2)}")
    # El MRE muestra que incluso con redondeo, podemos tener problemas
    assert abs(raw_total - 0.3) < 1e-10 or round(raw_total, 2) == 0.30

def test_mre_precision_accumulated():
    """MRE: Acumulación de errores de precisión con múltiples operaciones"""
    c = ShoppingCart()
    for _ in range(10):
        c.add_item(f"item_{_}", 1, 0.1)  # 10 items de 0.1 cada uno
    # Expectativa: 10 * 0.1 = 1.0
    # Realidad: Posible acumulación de errores de precisión
    assert round(c.calculate_total(), 2) == 1.00

def test_mre_precio_cero_indefinido():
    """MRE: Contrato no definido para precios cero o negativos"""
    c = Carrito()
    producto = Producto("test", 0.0)  # Precio cero
    # Expectativa: ¿Debería permitirse precio 0?
    # Realidad: Comportamiento no especificado en contrato
    c.agregar_producto(producto, 1)  # Usar API correcta
    assert c.calcular_total() >= 0  # Comportamiento asumido

def test_mre_precision_carrito_vs_shopping_cart():
    """MRE: Diferencias de precisión entre implementaciones"""
    # Carrito implementation
    c1 = Carrito()
    p1 = Producto("x", 0.1)
    c1.agregar_producto(p1, 3)  # 3 * 0.1 = 0.3
    
    # ShoppingCart implementation  
    c2 = ShoppingCart()
    c2.add_item("x", 3, 0.1)  # 3 * 0.1 = 0.3
    
    # Expectativa: Ambos deberían dar el mismo resultado
    # Realidad: Posibles diferencias en manejo de precisión
    assert round(c1.calcular_total(), 2) == round(c2.calculate_total(), 2)