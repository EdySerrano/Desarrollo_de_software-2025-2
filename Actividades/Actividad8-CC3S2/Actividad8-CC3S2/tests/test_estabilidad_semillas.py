"""
D1. Estabilidad con datos aleatorios controlados
Demuestra que con semillas fijas, dos corridas producen resultados idénticos
"""
import random
import pytest
from faker import Faker
from src.factories import ProductoFactory
from src.carrito import Carrito, ItemCarrito

def test_estabilidad_semillas_basico(capsys):
    """Test básico de estabilidad con semillas fijas"""
    # Primera corrida
    random.seed(123)
    Faker.seed(123)  # Semilla global necesaria para factory_boy
    
    p1 = ProductoFactory()
    c1 = Carrito()
    c1.agregar_producto(p1, 2)
    total1 = c1.calcular_total()
    print(f"Producto: {p1.nombre}, Precio: {p1.precio}, Total: {total1}")
    out1 = capsys.readouterr().out

    # Segunda corrida (mismas semillas)
    random.seed(123)
    Faker.seed(123)  # Resetear semilla global
    
    p2 = ProductoFactory()
    c2 = Carrito()
    c2.agregar_producto(p2, 2)
    total2 = c2.calcular_total()
    print(f"Producto: {p2.nombre}, Precio: {p2.precio}, Total: {total2}")
    out2 = capsys.readouterr().out

    # Verificaciones de estabilidad
    assert out1 == out2, "Las salidas deben ser idénticas con semillas fijas"
    assert p1.nombre == p2.nombre, "Nombres deben ser iguales con misma semilla"
    assert p1.precio == p2.precio, "Precios deben ser iguales con misma semilla"
    assert total1 == total2, "Totales deben ser iguales con misma semilla"

def test_estabilidad_multiples_productos(capsys):
    """Test de estabilidad con múltiples productos aleatorios"""
    def generar_carrito_aleatorio():
        carrito = Carrito()
        for i in range(5):  # 5 productos aleatorios
            producto = ProductoFactory()
            cantidad = random.randint(1, 10)
            carrito.agregar_producto(producto, cantidad)
        return carrito

    # Primera corrida
    random.seed(456)
    Faker.seed(456)
    
    c1 = generar_carrito_aleatorio()
    total1 = c1.calcular_total()
    print(f"Items: {len(c1.items)}, Total: {total1:.2f}")
    out1 = capsys.readouterr().out

    # Segunda corrida (mismas semillas)
    random.seed(456)
    Faker.seed(456)
    
    c2 = generar_carrito_aleatorio()
    total2 = c2.calcular_total()
    print(f"Items: {len(c2.items)}, Total: {total2:.2f}")
    out2 = capsys.readouterr().out

    # Verificaciones
    assert out1 == out2, "Salidas deben ser idénticas con semillas fijas"
    assert len(c1.items) == len(c2.items), "Número de items debe coincidir"
    assert total1 == total2, "Totales deben ser iguales"

def test_inestabilidad_sin_semillas():
    """Test que demuestra inestabilidad sin semillas fijas"""
    def generar_producto_aleatorio():
        return ProductoFactory()

    # Dos corridas sin fijar semillas
    p1 = generar_producto_aleatorio()
    p2 = generar_producto_aleatorio()
    
    # Es muy improbable que sean iguales sin semillas
    # (aunque teóricamente posible, por eso usamos skip si coinciden)
    if p1.nombre == p2.nombre and p1.precio == p2.precio:
        pytest.skip("Coincidencia aleatoria improbable - skip test")
    
    assert p1.nombre != p2.nombre or p1.precio != p2.precio, \
        "Sin semillas fijas, productos deben ser diferentes"

def test_estabilidad_con_descuentos(capsys):
    """Test de estabilidad con operaciones de descuento aleatorias"""
    # Primera corrida
    random.seed(789)
    Faker.seed(789)
    
    c1 = Carrito()
    for _ in range(3):
        producto = ProductoFactory()
        cantidad = random.randint(1, 5)
        c1.agregar_producto(producto, cantidad)
    
    descuento = random.uniform(0.1, 0.5)  # 10-50% descuento
    c1.aplicar_descuento(descuento)
    total1 = c1.calcular_total()
    
    print(f"Descuento: {descuento:.2%}, Total: {total1:.2f}")
    out1 = capsys.readouterr().out

    # Segunda corrida (mismas semillas)
    random.seed(789)
    Faker.seed(789)
    
    c2 = Carrito()
    for _ in range(3):
        producto = ProductoFactory()
        cantidad = random.randint(1, 5)
        c2.agregar_producto(producto, cantidad)
    
    descuento2 = random.uniform(0.1, 0.5)
    c2.aplicar_descuento(descuento2)
    total2 = c2.calcular_total()
    
    print(f"Descuento: {descuento2:.2%}, Total: {total2:.2f}")
    out2 = capsys.readouterr().out

    # Verificaciones
    assert out1 == out2, "Salidas con descuentos deben ser idénticas"
    assert descuento == descuento2, "Descuentos deben coincidir"
    assert total1 == total2, "Totales con descuento deben coincidir"