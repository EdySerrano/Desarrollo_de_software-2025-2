from src.carrito import Carrito, ItemCarrito, Producto

def test_redondeo_acumulado_vs_final():
    # Arrange
    c = Carrito()
    c.agregar_producto(Producto("a", 0.3333), 3)
    c.agregar_producto(Producto("b", 0.6667), 3)
    # Act
    total = c.calcular_total()
    suma_por_item = sum(i.producto.precio * i.cantidad for i in c.items)
    redondeo_por_item = sum(round(i.producto.precio * i.cantidad, 2) for i in c.items)
    redondeo_final = round(suma_por_item, 2)
    # Assert
    assert round(total, 2) == round(suma_por_item, 2)
    
    # Documentar diferencias para análisis
    print(f"Suma exacta por ítem: {suma_por_item}")
    print(f"Suma redondeando por ítem: {redondeo_por_item}")
    print(f"Redondeo final: {redondeo_final}")
    print(f"Diferencia (redondeo por ítem vs final): {redondeo_por_item - redondeo_final}")

def test_ejemplo_diferencia_clara():
    # Arrange - caso diseñado para mostrar diferencia clara
    c = Carrito()
    # Precios que cuando se redondean individualmente vs al final dan diferente resultado
    c.agregar_producto(Producto("item1", 0.125), 4)  # 0.125 * 4 = 0.50
    c.agregar_producto(Producto("item2", 0.124), 4)  # 0.124 * 4 = 0.496
    # Act
    suma_exacta = sum(i.producto.precio * i.cantidad for i in c.items)
    redondeo_por_item = sum(round(i.producto.precio * i.cantidad, 2) for i in c.items)
    redondeo_final = round(suma_exacta, 2)
    
    print(f"\nEjemplo con diferencia clara:")
    print(f"Item1: 0.125 * 4 = 0.50 -> redondeo: 0.50")
    print(f"Item2: 0.124 * 4 = 0.496 -> redondeo: 0.50")
    print(f"Suma exacta: {suma_exacta}")
    print(f"Redondeo por ítem: {redondeo_por_item}")
    print(f"Redondeo final: {redondeo_final}")
    print(f"Diferencia: {redondeo_por_item - redondeo_final}")
    
    # Assert
    assert abs(suma_exacta - 0.996) < 0.001

def test_casos_redondeo_diferencias():
    # Arrange - casos específicos que pueden mostrar diferencias
    casos = [
        # Caso 1: precios que al redondear individual vs final muestran diferencia
        [("item1", 0.335, 3), ("item2", 0.225, 4)],
        # Caso 2: precios en frontera de redondeo (0.5)
        [("item3", 1.225, 2), ("item4", 0.375, 4)],
        # Caso 3: múltiples decimales que acumulan error
        [("item5", 0.334, 3), ("item6", 0.667, 3)],
        # Caso 4: casos extremos
        [("item7", 0.999, 1), ("item8", 0.001, 100)],
    ]
    
    for i, caso in enumerate(casos):
        # Arrange
        c = Carrito()
        for nombre, precio, cantidad in caso:
            c.agregar_producto(Producto(nombre, precio), cantidad)     
        # Act
        total = c.calcular_total()
        suma_por_item = sum(item.producto.precio * item.cantidad for item in c.items)
        redondeo_por_item = sum(round(item.producto.precio * item.cantidad, 2) for item in c.items)
        redondeo_final = round(suma_por_item, 2)
        # Assert
        print(f"\nCaso {i+1}:")
        print(f"  Suma exacta: {suma_por_item}")
        print(f"  Redondeo por ítem: {redondeo_por_item}")
        print(f"  Redondeo final: {redondeo_final}")
        print(f"  Diferencia: {redondeo_por_item - redondeo_final}")
        
        # Verificar que el total calculado coincide con la suma exacta
        assert abs(total - suma_por_item) < 0.0001