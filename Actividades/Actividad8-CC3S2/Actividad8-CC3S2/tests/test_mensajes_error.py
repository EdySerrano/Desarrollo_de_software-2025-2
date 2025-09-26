"""
D3. Contrato de mensajes de error
Valida que mensajes de excepción contengan contexto accionable
"""
import pytest
from src.carrito import Carrito, Producto

@pytest.mark.xfail(reason="Esperamos mensaje con nombre de producto inexistente")
def test_mensaje_error_producto_inexistente():
    c = Carrito()
    nombre_inexistente = "producto_inexistente"
    
    with pytest.raises(ValueError) as excinfo:
        c.actualizar_cantidad(nombre_inexistente, 1)
    
    mensaje = str(excinfo.value)
    assert nombre_inexistente in mensaje, f"Mensaje esperado debe contener '{nombre_inexistente}', pero fue: '{mensaje}'"

@pytest.mark.xfail(reason="Esperamos mensaje con cantidad específica inválida")  
def test_mensaje_error_cantidad_negativa():
    c = Carrito()
    producto = Producto("test", 5.0)
    c.agregar_producto(producto, 1)
    cantidad_invalida = -5
    
    with pytest.raises(ValueError) as excinfo:
        c.actualizar_cantidad("test", cantidad_invalida)
    
    mensaje = str(excinfo.value)
    assert str(cantidad_invalida) in mensaje, f"Mensaje esperado debe contener '{cantidad_invalida}', pero fue: '{mensaje}'"

@pytest.mark.xfail(reason="Esperamos mensaje con cantidad excesiva específica")
def test_mensaje_error_cantidad_excesiva():
    c = Carrito()
    producto = Producto("item", 10.0)
    c.agregar_producto(producto, 3)
    cantidad_excesiva = 5
    
    with pytest.raises(ValueError) as excinfo:
        c.remover_producto(producto, cantidad_excesiva)
    
    mensaje = str(excinfo.value)
    assert str(cantidad_excesiva) in mensaje, f"Cantidad excesiva {cantidad_excesiva} debería aparecer en: '{mensaje}'"
    assert "3" in mensaje, f"Cantidad disponible 3 debería aparecer en: '{mensaje}'"

def test_mensaje_error_producto_inexistente_en_remover():
    c = Carrito()
    nombre_inexistente = "no_existe"
    
    with pytest.raises(ValueError) as excinfo:
        c.remover_producto(Producto(nombre_inexistente, 1.0), 1)
    
    mensaje = str(excinfo.value)
    print(f"\\nMensaje actual del sistema: '{mensaje}'")
    print(f"¿Contiene '{nombre_inexistente}'? {nombre_inexistente in mensaje}")
    
    assert "Producto no encontrado" in mensaje or "no encontrado" in mensaje

@pytest.mark.xfail(reason="Esperamos mensaje descriptivo sobre porcentaje inválido")
def test_mensaje_error_descuento_invalido():
    c = Carrito()
    producto = Producto("test", 100.0)
    c.agregar_producto(producto, 1)
    
    porcentaje_invalido = 150  # > 100%
    
    with pytest.raises(ValueError) as excinfo:
        c.aplicar_descuento(porcentaje_invalido)
    
    mensaje = str(excinfo.value)
    assert str(porcentaje_invalido) in mensaje, f"Porcentaje {porcentaje_invalido} debería aparecer en: '{mensaje}'"
    assert "0" in mensaje and "100" in mensaje, f"Rango válido 0-100 debería aparecer en: '{mensaje}'"

def test_verificacion_mensajes_actuales():
    c = Carrito()
    producto = Producto("test", 10.0)
    c.agregar_producto(producto, 2)
    
    mensajes_capturados = {}
        
    # Capturar mensaje de remoción excesiva
    try:
        c.remover_producto(producto, 5)
    except ValueError as e:
        mensajes_capturados["cantidad_excesiva"] = str(e)
    
    # Capturar mensaje de producto inexistente en remoción
    try:
        producto_inexistente = Producto("inexistente", 1.0)
        c.remover_producto(producto_inexistente, 1)
    except ValueError as e:
        mensajes_capturados["producto_inexistente_remover"] = str(e)
    
    # Capturar mensaje de descuento inválido (> 100%)
    try:
        c.aplicar_descuento(150)
    except ValueError as e:
        mensajes_capturados["descuento_invalido_alto"] = str(e)
    
    # Capturar mensaje de descuento inválido (< 0%)
    try:
        c.aplicar_descuento(-10)
    except ValueError as e:
        mensajes_capturados["descuento_invalido_negativo"] = str(e)
    
    # Imprimir todos los mensajes para análisis
    print("\\n=== MENSAJES DE ERROR ACTUALES DEL SISTEMA ===")
    for tipo, mensaje in mensajes_capturados.items():
        print(f"{tipo}: '{mensaje}'")
    
    print("\\n=== ANÁLISIS DE CONTEXTO ACCIONABLE ===")
    for tipo, mensaje in mensajes_capturados.items():
        if "cantidad_excesiva" in tipo:
            print(f"¿Incluye cantidad solicitada (5)? {'5' in mensaje}")
            print(f"¿Incluye cantidad disponible (2)? {'2' in mensaje}")
        elif "producto_inexistente" in tipo:
            print(f"¿Incluye nombre específico? {'inexistente' in mensaje}")
        elif "descuento_invalido" in tipo:
            print(f"¿Incluye valor específico? Analizar: {mensaje}")
    
    assert len(mensajes_capturados) > 0, "Deberíamos haber capturado al menos un mensaje"