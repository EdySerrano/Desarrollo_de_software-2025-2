"""Pytest tests for design patterns (Singleton, Prototype).

Estos tests cargan las implementaciones existentes por ruta de archivo para
evitar dependencias en paquetes: `ConfigSingleton` y `NullResourceFactory`.
"""
import importlib.util
import os
from pathlib import Path


def load_from_path(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore
    return module


# Rutas a los modulos existentes
# Calculamos la raiz `Actividad14-CC3S2` subiendo 2 niveles desde `Ejercicio3.3`.
ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "Fase2"
SINGLETON_PY = BASE / "Ejercicio2.1" / "singleton.py"
FACTORY_PY = BASE / "Ejercicio2.2" / "factory.py"


def test_singleton_meta():
    mod = load_from_path("singleton_mod", str(SINGLETON_PY))
    ConfigSingleton = mod.ConfigSingleton
    a = ConfigSingleton("X")
    b = ConfigSingleton("Y")
    assert a is b


def test_prototype_clone_independent():
    # Cargamos la fabrica de NullResource
    factory_mod = load_from_path("factory_mod", str(FACTORY_PY))
    NullResourceFactory = factory_mod.NullResourceFactory

    # Importamos ResourcePrototype desde el modulo local (mismo directorio)
    proto_mod = load_from_path("proto_mod", str(Path(__file__).parent / "prototype.py"))
    ResourcePrototype = proto_mod.ResourcePrototype

    proto = ResourcePrototype(NullResourceFactory.create("app"))

    # Mutators que aniaden claves distintas
    c1 = proto.clone(lambda b: b.__setitem__("f1", 1))
    c2 = proto.clone(lambda b: b.__setitem__("b1", 2))

    # Aseguramos independencia: c1 no debe tener b1 y c2 no debe tener f1
    assert "f1" not in c2.data and "b1" not in c1.data
