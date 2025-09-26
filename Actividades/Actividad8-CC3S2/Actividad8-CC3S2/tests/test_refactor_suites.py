import pytest
from unittest.mock import Mock
from src.shopping_cart import ShoppingCart


class TestPrecisionMonetaria:
    """Suite de pruebas enfocada en la precisión monetaria y cálculos financieros"""
    
    def test_suma_pequenas_cantidades(self):
        # Arrange
        cart = ShoppingCart()
        cart.add_item("x", 1, 0.05)  # nombre, cantidad, precio unitario
        cart.add_item("y", 1, 0.05)  # segundo item con mismo precio
        # Act
        total = cart.calculate_total()      
        # Assert
        assert round(total, 2) == 0.10

    def test_precision_con_decimales(self):
        # Arrange
        cart = ShoppingCart()
        cart.add_item("item1", 3, 0.33)  # 3 * 0.33 = 0.99
        cart.add_item("item2", 1, 0.01)  # 1 * 0.01 = 0.01  
        # Act
        total = cart.calculate_total()      
        # Assert
        assert round(total, 2) == 1.00

    def test_aplicacion_descuento_precision(self):
        # Arrange
        cart = ShoppingCart()
        cart.add_item("item", 3, 3.33)  # 3 * 3.33 = 9.99
        cart.apply_discount(10)  # 10% de descuento
        # Act
        total = cart.calculate_total()
        # Assert
        expected = round(9.99 * 0.9, 2)  # 8.991 -> 8.99
        assert total == expected