#!/usr/bin/env python3
"""Ejercicio 2.3: Clonar prototipo y añadir bloque local_file.

Genera `terraform/welcome.tf.json` con un recurso `null_resource` clonado
que contiene un trigger `welcome` y añade un recurso `local_file` que escribirá
`bienvenida.txt` en el módulo cuando se aplique con Terraform.
"""

import json
import os

from iac_patterns.prototype import ResourcePrototype
from iac_patterns.factory import NullResourceFactory


def add_welcome_file(block: dict) -> None:
    """Mutator que añade trigger 'welcome' y un bloque local_file al recurso.

    La estructura interna se adapta al formato usado por las fábricas en este repo:
    - block["resource"][0]["null_resource"][0] -> dict con la clave del recurso
    - Añadimos el trigger en esa ubicación y añadimos un nuevo elemento a
      block["resource"] con la definición de `local_file`.
    """
    # Accede al bloque null_resource dentro del dict
    res_block = block["resource"][0]["null_resource"][0]

    # Nombre del recurso (por ejemplo 'app_0')
    resource_name = next(iter(res_block.keys()))

    # Añade el trigger de bienvenida
    res_block[resource_name][0].setdefault("triggers", {})
    res_block[resource_name][0]["triggers"]["welcome"] = "¡Hola!"

    # Añade el bloque local_file como otro elemento en la lista `resource`
    local_block = {
        "local_file": [
            {
                "welcome_txt": [
                    {
                        "content": "Bienvenido",
                        "filename": "${path.module}/bienvenida.txt"
                    }
                ]
            }
        ]
    }

    block.setdefault("resource", []).append(local_block)


def main():
    # Crea un prototipo base con nombre 'app_0'
    base = ResourcePrototype(NullResourceFactory.create("app_0"))

    # Clona y aplica la mutación
    cloned = base.clone(add_welcome_file).data

    # Escribe el archivo JSON en terraform/welcome.tf.json
    out_dir = "terraform"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "welcome.tf.json")
    with open(out_path, "w") as f:
        json.dump(cloned, f, indent=4)

    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()
