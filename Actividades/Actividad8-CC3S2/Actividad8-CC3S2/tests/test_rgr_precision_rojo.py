import pytest
from src.shopping_cart import ShoppingCart

@pytest.mark.xfail(reason="Float binario puede introducir error en dinero")
def test_total_precision_decimal():
    # Arrange
    cart = ShoppingCart()
    # Usando valores que causan problemas de precisión incluso con redondeo
    cart.add_item("x", 3, 0.1)  # 0.3
    cart.add_item("y", 1, 0.03) # 0.03
    # Total debería ser 0.33, pero puede haber error de precisión
    # Act
    total = cart.calculate_total()
    # Assert
    # Este test debe fallar debido a errores de precisión de punto flotante
    assert total == 0.33000000000000007  # valor exacto que produce el error de precisión

@pytest.mark.xfail(reason="Demostración directa del problema de precisión binaria")
def test_precision_binaria_directa():
    # Arrange
    cart = ShoppingCart()
    # Caso clásico: 0.1 + 0.2 != 0.3 en binario
    cart.add_item("item1", 1, 0.1)
    cart.add_item("item2", 1, 0.2)    
    # Act - calculamos sin redondeo para mostrar el problema
    raw_total = sum(item["cantidad"] * item["precio_x_unidad"] for item in cart.items.values())    
    # Assert - esto debe fallar porque 0.1 + 0.2 != 0.3 exactamente
    assert raw_total == 0.3  # Fallará por precisión binaria