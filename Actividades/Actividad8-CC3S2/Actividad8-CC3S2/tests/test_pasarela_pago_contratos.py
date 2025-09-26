import pytest
from unittest.mock import Mock
from src.shopping_cart import ShoppingCart

def test_pago_exitoso():
    # Arrange
    pg = Mock()
    pg.process_payment.return_value = True
    cart = ShoppingCart(payment_gateway=pg)
    cart.add_item("x", 1, 10.0)  # nombre, cantidad, precio
    total = cart.calculate_total()
    # Act
    resultado = cart.process_payment(total)
    # Assert
    assert resultado is True
    pg.process_payment.assert_called_once_with(total)

def test_pago_rechazo_definitivo():
    # Arrange
    pg = Mock()
    pg.process_payment.return_value = False
    cart = ShoppingCart(payment_gateway=pg)
    cart.add_item("x", 1, 10.0)
    total = cart.calculate_total()
    # Act
    resultado = cart.process_payment(total)
    # Assert
    assert resultado is False
    pg.process_payment.assert_called_once_with(total)

def test_pago_excepcion_invalida():
    # Arrange
    pg = Mock()
    pg.process_payment.side_effect = ValueError("Tarjeta inválida")
    cart = ShoppingCart(payment_gateway=pg)
    cart.add_item("servicio", 1, 50.0)
    total = cart.calculate_total()
    # Act / Assert
    with pytest.raises(ValueError, match="Tarjeta inválida"):
        cart.process_payment(total)   
    # Verificar que se llama una sola vez (sin reintentos)
    assert pg.process_payment.call_count == 1

def test_pago_con_monto_cero():
    # Arrange
    pg = Mock()
    pg.process_payment.return_value = True
    cart = ShoppingCart(payment_gateway=pg)
    # No agregar items, total será 0.0
    total = cart.calculate_total()   
    # Act
    resultado = cart.process_payment(total)
    # Assert
    assert resultado is True
    assert total == 0.0
    pg.process_payment.assert_called_once_with(0.0)