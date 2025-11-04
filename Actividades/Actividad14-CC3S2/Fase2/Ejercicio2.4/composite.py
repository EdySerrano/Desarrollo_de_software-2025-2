#!/usr/bin/env python3
"""Ejercicio 2.4: Generar export con submódulos 'network' y 'app'."""

import json
import os

from iac_patterns.composite import CompositeModule


def main():
    cm = CompositeModule()

    # Añadimos dos submódulos simples; en TF JSON los módulos se expresan como
    # "module": { "name": [ { <config> } ] }
    network_module = {
        "module": {
            "network": [
                {
                    "source": "./modules/network",
                    "cidr": "10.0.0.0/16"
                }
            ]
        }
    }

    app_module = {
        "module": {
            "app": [
                {
                    "source": "./modules/app",
                    "replicas": 2
                }
            ]
        }
    }

    cm.add(network_module)
    cm.add(app_module)

    exported = cm.export()

    out_dir = "terraform"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "submodules.tf.json")
    with open(out_path, "w") as f:
        json.dump(exported, f, indent=4)

    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()
