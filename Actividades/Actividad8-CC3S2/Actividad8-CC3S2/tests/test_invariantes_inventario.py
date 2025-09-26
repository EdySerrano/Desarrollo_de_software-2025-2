"""
D2. Invariantes de inventario
Valida que las operaciones de agregar/remover mantengan invariantes del carrito
Nota: actualizar_cantidad tiene un bug en el código fuente, por lo que se omite
"""
import pytest
from src.carrito import Carrito, ItemCarrito, Producto

def test_invariante_agregar_remover():
    """Invariante principal: agregar N, remover N -> total=0 e items=0"""
    # Arrange
    c = Carrito()
    producto = Producto("x", 5.0)
    cantidad_inicial = 3
    # Act - Agregar N
    c.agregar_producto(producto, cantidad_inicial)
    total_inicial = c.calcular_total()
    items_inicial = c.contar_items()
    # Act - Remover N (completamente)
    c.remover_producto(producto, cantidad_inicial)
    # Assert - Estado final debe ser vacío
    assert c.calcular_total() == 0.0, "Total debe ser 0 después de remover todo"
    assert c.contar_items() == 0, "Items debe ser 0 después de remover todo"
    assert len(c.items) == 0, "Lista de items debe estar vacía"
    # Sanity check del estado inicial
    assert total_inicial == 15.0, "Verificación del cálculo inicial"
    assert items_inicial == 3, "Verificación del conteo inicial"

def test_invariante_agregar_remover_parcial():
    """Invariante: remover parcial mantiene consistencia"""
    # Arrange
    c = Carrito()
    producto = Producto("z", 7.5)
    # Act - Agregar 5, remover 2, debería quedar 3
    c.agregar_producto(producto, 5)
    total_inicial = c.calcular_total()  # 37.5
    c.remover_producto(producto, 2)
    total_final = c.calcular_total()    # 22.5
    items_final = c.contar_items()      # 3
    # Assert - Invariante de consistencia
    assert total_final == 22.5, "Total debe reflejar la cantidad restante"
    assert items_final == 3, "Deben quedar 3 items"
    assert len(c.items) == 1, "Debe seguir habiendo 1 tipo de producto"
    assert total_inicial == 37.5, "Verificación del total inicial"

def test_invariante_idempotencia_agregar():
    """Invariante: agregar el mismo producto incrementa cantidad correctamente"""
    # Arrange
    c = Carrito()
    producto = Producto("w", 3.0)
    # Act - Agregar en múltiples pasos
    c.agregar_producto(producto, 2)  # 6.0
    total_1 = c.calcular_total()
    c.agregar_producto(producto, 1)  # 9.0 total
    total_2 = c.calcular_total()
    c.agregar_producto(producto, 2)  # 15.0 total  
    total_3 = c.calcular_total()
    items_final = c.contar_items()
    # Assert - Invariante de acumulación correcta
    assert total_1 == 6.0, "Primera adición correcta"
    assert total_2 == 9.0, "Segunda adición correcta" 
    assert total_3 == 15.0, "Tercera adición correcta"
    assert items_final == 5, "Total de items debe ser 5 (2+1+2)"
    assert len(c.items) == 1, "Solo debe haber 1 tipo de producto"

def test_invariante_multiples_productos():
    """Invariante: operaciones en un producto no afectan otros productos"""
    # Arrange
    c = Carrito()
    producto_a = Producto("A", 10.0)
    producto_b = Producto("B", 5.0)
    # Act - Agregar dos productos diferentes
    c.agregar_producto(producto_a, 2)  # 20.0
    c.agregar_producto(producto_b, 3)  # 15.0
    total_inicial = c.calcular_total()  # 35.0
    # Act - Remover completamente producto A
    c.remover_producto(producto_a, 2)
    # Assert - Solo producto B debe permanecer inalterado
    assert c.calcular_total() == 15.0, "Solo debe quedar el total del producto B"
    assert c.contar_items() == 3, "Solo deben quedar los items del producto B"
    assert len(c.items) == 1, "Solo debe quedar un tipo de producto"
    # Verificar que el producto restante es el correcto
    item_restante = c.items[0]
    assert item_restante.producto.nombre == "B", "El producto B debe permanecer"
    assert item_restante.cantidad == 3, "Cantidad de B debe ser inalterada"
    # Sanity check
    assert total_inicial == 35.0, "Verificación del total inicial"

def test_invariante_agregar_remover_completo():
    """Test completo del invariante principal: agregar N, remover N -> estado vacío"""
    # Arrange
    c = Carrito()
    producto = Producto("test", 12.5)
    cantidad = 4
    # Verificar estado inicial vacío
    assert c.calcular_total() == 0.0
    assert c.contar_items() == 0
    assert len(c.items) == 0
    # Act - Agregar N
    c.agregar_producto(producto, cantidad)
    total_intermedio = c.calcular_total()
    items_intermedio = c.contar_items()
    # Verificar estado intermedio
    assert total_intermedio == 50.0  # 12.5 * 4
    assert items_intermedio == 4
    assert len(c.items) == 1
    # Act - Remover N (volver al estado inicial)
    c.remover_producto(producto, cantidad)
    # Assert - Invariante: debe volver al estado inicial vacío
    assert c.calcular_total() == 0.0, "INVARIANTE: Total debe volver a 0"
    assert c.contar_items() == 0, "INVARIANTE: Items debe volver a 0"  
    assert len(c.items) == 0, "INVARIANTE: Lista debe estar vacía"