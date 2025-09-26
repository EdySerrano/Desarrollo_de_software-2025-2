import pytest
from src.carrito import Carrito, ItemCarrito, Producto

@pytest.mark.parametrize("precio", [0.01, 0.005, 0.0049, 9999999.99])
def test_precios_frontera(precio):
    # Arrange
    c = Carrito()
    producto = Producto("p", precio)
    # Act
    c.agregar_producto(producto, 1)
    # Assert
    assert c.calcular_total() >= 0  # ajusta si el contrato define otra cosa

@pytest.mark.xfail(reason="Contrato no definido para precio=0 o negativo")
@pytest.mark.parametrize("precio_invalido", [0.0, -1.0])
def test_precios_invalidos(precio_invalido):
    # Arrange
    c = Carrito()
    # Act
    producto = Producto("p", precio_invalido)
    c.agregar_producto(producto, 1)
    # Assert
    # Esta prueba puede fallar o pasar dependiendo del comportamiento del SUT