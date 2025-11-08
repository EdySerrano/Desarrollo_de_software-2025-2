#!/usr/bin/env python3
"""Simple mediador que consulta los outputs de los módulos y establece
dependencias (triggers) antes de generar `main.tf.json`.

Comportamiento:
 - Crea la red (NetworkFactoryModule) y obtiene su output (DependsOn).
 - Crea el servidor (ServerFactoryModule) pasando la dependencia de la red.
 - Crea el firewall (FirewallFactoryModule) pasando la dependencia del servidor.
 - Fusiona los bloques `resource` en un solo diccionario y escribe `main.tf.json`.
"""
import json
from pathlib import Path

from dependency import DependsOn
from network import NetworkFactoryModule
from server import ServerFactoryModule
from firewall import FirewallFactoryModule


class Mediator:
    """Mediador que orquesta la creación de módulos con dependencias."""
    def __init__(self):
        self.order = []

    def build(self):
        # Crear la red y obtener su output/estado
        net = NetworkFactoryModule()
        net_block = net.build()
        net_out = net.outputs()  # DependsOn object
        self.order.append(net_block)

        # Crear el servidor indicando la dependencia en la red
        srv = ServerFactoryModule(depends=net_out)
        srv_block = srv.build()
        srv_out = srv.outputs()
        self.order.append(srv_block)

        # Crear el firewall indicando la dependencia en el servidor
        fw = FirewallFactoryModule(depends=srv_out)
        fw_block = fw.build()
        fw_out = fw.outputs()
        self.order.append(fw_block)

        # Merge resources
        merged = {"terraform": {"required_providers": {}}, "resource": {}}
        for block in self.order:
            for res_type, res_defs in block.get("resource", {}).items():
                merged_resources = merged["resource"].setdefault(res_type, {})
                merged_resources.update(res_defs)

        return merged


def main():
    mediator = Mediator()
    cfg = mediator.build()
    out_path = Path("main.tf.json")
    out_path.write_text(json.dumps(cfg, indent=2))
    print(f"{out_path} generado.")


if __name__ == "__main__":
    main()
