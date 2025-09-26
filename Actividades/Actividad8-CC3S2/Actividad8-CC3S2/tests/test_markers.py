import pytest
from src.carrito import Carrito, ItemCarrito, Producto
from src.shopping_cart import ShoppingCart

@pytest.mark.smoke
def test_smoke_agregar_y_total():
    # Arrange
    c = Carrito()
    producto = Producto("x", 1.0)
    # Act
    c.agregar_producto(producto, 1)
    # Assert
    assert c.calcular_total() == 1.0

@pytest.mark.smoke
def test_smoke_shopping_cart_basico():
    # Arrange
    cart = ShoppingCart()  
    # Act
    cart.add_item("producto", 1, 5.0)
    total = cart.calculate_total()
    # Assert
    assert total == 5.0

@pytest.mark.smoke
def test_smoke_pago_exitoso():
    # Arrange
    from unittest.mock import Mock
    pg = Mock()
    pg.process_payment.return_value = True
    cart = ShoppingCart(payment_gateway=pg)
    cart.add_item("item", 1, 10.0)
    # Act
    resultado = cart.process_payment(10.0) 
    # Assert
    assert resultado is True

@pytest.mark.regression
def test_regression_descuento_redondeo():
    # Arrange
    c = Carrito()
    producto = Producto("x", 10.0)
    c.agregar_producto(producto, 1)
    # Act
    total_con_descuento = c.aplicar_descuento(15)  # 15% de descuento
    # Assert
    assert round(total_con_descuento, 2) == 8.50

@pytest.mark.regression
def test_regression_precision_acumulada():
    # Arrange
    c = Carrito()
    c.agregar_producto(Producto("a", 0.1), 3)
    c.agregar_producto(Producto("b", 0.2), 2)
    # Act
    total = c.calcular_total()
    # Assert
    # 0.1*3 + 0.2*2 = 0.3 + 0.4 = 0.7
    assert round(total, 2) == 0.70

@pytest.mark.regression
def test_regression_actualizacion_cantidad():
    # Arrange
    c = Carrito()
    producto = Producto("test", 5.0)
    c.agregar_producto(producto, 2)  # 2 * 5.0 = 10.0
    # Act
    c.actualizar_cantidad(producto, 3)  # Cambiar a 3
    total = c.calcular_total()
    # Assert
    assert total == 15.0  # 3 * 5.0

@pytest.mark.regression
def test_regression_multiples_descuentos():
    # Arrange
    cart = ShoppingCart()
    cart.add_item("producto1", 2, 10.0)  # 20.0
    cart.add_item("producto2", 1, 15.0)  # 15.0
    # Total: 35.0
    # Act
    cart.apply_discount(20)  # 20% de descuento
    total = cart.calculate_total()
    # Assert
    expected = 35.0 * 0.8  # 28.0
    assert total == 28.0

@pytest.mark.regression
def test_regression_casos_frontera():
    # Arrange
    c = Carrito()
    c.agregar_producto(Producto("precio_pequeño", 0.01), 100)
    # Act
    total = c.calcular_total()
    # Assert
    assert total == 1.0  # 0.01 * 100
