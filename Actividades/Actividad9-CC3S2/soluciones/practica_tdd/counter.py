"""
counter.py
Servicio Flask que implementa un contador in-memory.
Provee rutas para crear, leer, actualizar e eliminar contadores.
"""

import status
from flask import Flask, request
from functools import wraps

app = Flask(__name__)

# Diccionario global que guarda el nombre de cada contador y su valor.
COUNTERS = {}

def change_counter(name, delta):
    """
    Función auxiliar que modifica el valor de un contador por un delta.
    """
    COUNTERS[name] += delta
    return {name: COUNTERS[name]}

def require_counter(func):
    """
    Decorador que verifica que el contador exista antes de ejecutar la función.
    Si no existe, retorna 404 NOT FOUND.
    """
    @wraps(func)
    def wrapper(name, *args, **kwargs):
        if name not in COUNTERS:
            return {"message": f"El contador '{name}' no existe"}, status.HTTP_404_NOT_FOUND
        return func(name, *args, **kwargs)
    return wrapper

@app.route("/counters", methods=["GET"])
def list_counters():
    """
    Lista todos los contadores existentes.
    Retorna 200 (OK) con un diccionario de todos los contadores.
    """
    app.logger.info("Solicitud para listar todos los contadores")
    return COUNTERS, status.HTTP_200_OK

@app.route("/counters/<name>", methods=["POST"])
def create_counter(name):
    """
    Crea un nuevo contador con valor inicial = 0.
    Retorna 201 (CREATED) si se crea correctamente.
    Retorna 409 (CONFLICT) si el contador ya existía.
    """
    app.logger.info(f"Solicitud para crear el contador: {name}")
    global COUNTERS

    if name in COUNTERS:
        return {"message": f"El contador '{name}' ya existe"}, status.HTTP_409_CONFLICT

    COUNTERS[name] = 0
    return {name: COUNTERS[name]}, status.HTTP_201_CREATED

@app.route("/counters/<name>", methods=["PUT"])
def update_counter(name):
    """
    Actualiza (p.e. incrementa) el contador <name>.
    Retorna 200 (OK) si se actualiza correctamente.
    Retorna 404 (NOT FOUND) si el contador no existe.
    """
    app.logger.info(f"Solicitud para actualizar el contador: {name}")
    global COUNTERS

    if name not in COUNTERS:
        return {"message": f"El contador '{name}' no existe"}, status.HTTP_404_NOT_FOUND

    # Ejemplo de actualización: incrementar en 1
    COUNTERS[name] += 1
    return {name: COUNTERS[name]}, status.HTTP_200_OK

@app.route("/counters/<name>", methods=["GET"])
def read_counter(name):
    """
    Lee el valor actual del contador <name>.
    Retorna 200 (OK) si el contador existe.
    Retorna 404 (NOT FOUND) si el contador no existe.
    """
    app.logger.info(f"Solicitud para leer el contador: {name}")
    global COUNTERS

    if name not in COUNTERS:
        return {"message": f"El contador '{name}' no existe"}, status.HTTP_404_NOT_FOUND

    return {name: COUNTERS[name]}, status.HTTP_200_OK

@app.route("/counters/<name>", methods=["DELETE"])
def delete_counter(name):
    """
    Elimina el contador <name>.
    Retorna 204 (NO CONTENT) si la eliminación es exitosa.
    Retorna 404 (NOT FOUND) si el contador no existe.
    """
    app.logger.info(f"Solicitud para eliminar el contador: {name}")
    global COUNTERS

    if name not in COUNTERS:
        return {"message": f"El contador '{name}' no existe"}, status.HTTP_404_NOT_FOUND

    del COUNTERS[name]
    # 204 NO CONTENT suele devolver un cuerpo vacío
    return "", status.HTTP_204_NO_CONTENT

@app.route("/counters/<name>/increment", methods=["PUT"])
@require_counter
def increment_counter(name):
    """
    Incrementa el contador <name> en 1 usando la función change_counter.
    Retorna 200 (OK) si se incrementa correctamente.
    Retorna 404 (NOT FOUND) si el contador no existe (manejado por el decorador).
    """
    app.logger.info(f"Solicitud para incrementar el contador: {name}")
    return change_counter(name, +1), status.HTTP_200_OK

@app.route("/counters/<name>/set", methods=["PUT"])
@require_counter
def set_counter(name):
    """
    Establece el contador <name> a un valor específico.
    Retorna 200 (OK) si se establece correctamente.
    Retorna 404 (NOT FOUND) si el contador no existe (manejado por el decorador).
    Retorna 400 (BAD REQUEST) si el valor no es válido.
    """
    app.logger.info(f"Solicitud para establecer el contador: {name}")
    body = request.get_json()
    
    # Validar que el valor sea entero y >= 0
    value = body.get("value")
    if not isinstance(value, int) or value < 0:
        return {"message": "El valor debe ser un entero mayor o igual a 0"}, status.HTTP_400_BAD_REQUEST
    
    COUNTERS[name] = value
    return {name: COUNTERS[name]}, status.HTTP_200_OK

@app.route("/counters/<name>/reset", methods=["PUT"])
@require_counter
def reset_counter(name):
    """
    Resetea el contador <name> a 0.
    Retorna 200 (OK) si se resetea correctamente.
    Retorna 404 (NOT FOUND) si el contador no existe (manejado por el decorador).
    """
    app.logger.info(f"Solicitud para resetear el contador: {name}")
    # Usar change_counter con delta negativo para reutilizar la lógica
    current_value = COUNTERS[name]
    return change_counter(name, -current_value), status.HTTP_200_OK
