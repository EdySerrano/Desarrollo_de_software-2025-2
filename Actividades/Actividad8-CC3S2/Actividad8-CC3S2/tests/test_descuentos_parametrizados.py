import pytest
from src.carrito import Carrito, ItemCarrito, Producto

@pytest.mark.parametrize(
    "precio,cantidad,descuento,esperado",
    [
        (10.00, 1, 0.00, 10.00),
        (10.00, 1, 0.01, 9.90),
        (10.01, 1, 0.3333, 6.67),  # ajusta 'esperado' si el contrato indica otro redondeo
        (100.00, 1, 0.5, 50.00),
        (1.00, 1, 0.9999, 0.00),
        (50.00, 1, 1.00, 0.00),
    ],
)
def test_descuento_total(precio, cantidad, descuento, esperado):
    # Arrange
    c = Carrito()
    producto = Producto("p", precio)
    c.agregar_producto(producto, cantidad)
    # Act
    total = c.aplicar_descuento(descuento * 100)  # convertir a porcentaje
    # Assert
    assert round(total, 2) == pytest.approx(esperado, abs=0.01)