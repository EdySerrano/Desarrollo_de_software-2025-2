"""Genera `main.tf.json` para flotas de tamaño dado y mide su tamaño en bytes.

Este script carga la `NullResourceFactory` desde Fase2/Ejercicio2.2 y la
implementación `ResourcePrototype` localizada en Fase3/Ejercicio3.3, clona el
prototipo N veces con un mutator que renombra recursos e inserta un trigger
`index`, y escribe los JSON resultantes y un log con su tamaño en bytes.
"""
import json
import os
from pathlib import Path
import importlib.util


def load_module_from_path(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore
    return mod


ROOT = Path(__file__).resolve().parents[2]  # Actividad14-CC3S2
FACTORY_PY = ROOT / "Fase2" / "Ejercicio2.2" / "factory.py"
PROTO_PY = ROOT / "Fase3" / "Ejercicio3.3" / "prototype.py"


def build_main(count: int) -> dict:
    factory_mod = load_module_from_path("factory_mod", FACTORY_PY)
    proto_mod = load_module_from_path("proto_mod", PROTO_PY)

    NullResourceFactory = factory_mod.NullResourceFactory
    ResourcePrototype = proto_mod.ResourcePrototype

    base_proto = ResourcePrototype(NullResourceFactory.create("placeholder"))

    combined_resources = []

    for i in range(count):
        def mutator(d, idx=i):
            res_block = d["resource"][0]["null_resource"][0]
            original_name = next(iter(res_block.keys()))
            new_name = f"{original_name}_{idx}"
            res_block[new_name] = res_block.pop(original_name)
            res_block[new_name][0].setdefault("triggers", {})
            res_block[new_name][0]["triggers"]["index"] = idx

        clone = base_proto.clone(mutator).data
        # clone is like {"resource": [ { ... } ] }
        combined_resources.append(clone["resource"][0])

    return {"resource": combined_resources}


def write_and_measure(count: int, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    main = build_main(count)
    out_path = out_dir / f"main_{count}.tf.json"
    with open(out_path, "w") as f:
        json.dump(main, f, indent=4)

    size = out_path.stat().st_size
    return out_path, size


def main():
    base = Path(__file__).parent
    out_dir = base / "terraform"
    results = []

    for n in (15, 150):
        path, size = write_and_measure(n, out_dir)
        results.append((n, path, size))

    # Escribe un log simple con los tamaños
    log_path = base / "size_log.txt"
    with open(log_path, "w") as f:
        for n, p, s in results:
            f.write(f"count={n} path={p} bytes={s}\n")

    # Print a short summary
    for n, p, s in results:
        print(f"Wrote: {p} ({s} bytes)")
    print(f"Log: {log_path}")


if __name__ == "__main__":
    main()
