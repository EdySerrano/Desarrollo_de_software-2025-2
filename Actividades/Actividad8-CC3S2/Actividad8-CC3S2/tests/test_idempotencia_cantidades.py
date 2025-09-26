from src.carrito import Carrito, ItemCarrito, Producto

def test_actualizacion_idempotente():
    # Arrange
    c = Carrito()
    producto = Producto("x", 3.25)
    c.agregar_producto(producto, 2)
    total1 = c.calcular_total()
    items_iniciales = c.contar_items()
    # Act
    for _ in range(5):
        c.actualizar_cantidad(producto, 2)
    total2 = c.calcular_total()
    items_finales = c.contar_items()
    # Assert
    assert total1 == total2
    assert items_iniciales == items_finales == 2
    assert sum(i.cantidad for i in c.items) == 2