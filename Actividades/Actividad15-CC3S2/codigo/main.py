#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
from pathlib import Path

OUTPUTS_FILE = "network/network_outputs.json"

class NetworkModuleOutput:
    """Lee las salidas publicadas por el módulo 'network'."""
    def __init__(self, outputs_path=OUTPUTS_FILE):
        path = Path(outputs_path)
        if not path.exists():
            raise FileNotFoundError(
                f"No se encontró {path}. Ejecuta primero 'terraform apply' en network/"
            )
        data = json.loads(path.read_text())
        try:
            self.name = data["outputs"]["name"]["value"]
            self.cidr = data["outputs"]["cidr"]["value"]
        except (KeyError, TypeError) as exc:
            raise KeyError(f"Formato inesperado en {path}") from exc

class ServerFactoryModule:
    """Define un null_resource que simula un servidor ligado a la subred."""
    def __init__(self, name, zone="local", outputs_path=OUTPUTS_FILE, server_config=None):
        """Inicializa la fábrica de servidores.

        server_config: dict opcional con parámetros adicionales del servidor
        (por ejemplo: {"display_name": "srv-1", "tags": {"env": "dev"}}).
        Estos parámetros se inyectan en los triggers como JSON para que Terraform
        los vea como parte del recurso y se puedan usar/visualizar.
        """
        self._name = name
        self._zone = zone
        self._network = NetworkModuleOutput(outputs_path)
        # Normalizar a dict (evita None)
        self._server_config = server_config or {}
        self.resources = self._build()

    def _build(self):
        # Construimos los triggers y añadimos server_config como JSON si existe
        triggers = {
            "server_name": self._name,
            "subnet_name": self._network.name,
            "subnet_cidr": self._network.cidr,
            "zone": self._zone
        }
        if self._server_config:
            # Importar localmente json para serializar de forma estable
            try:
                server_config_json = json.dumps(self._server_config, sort_keys=True)
            except Exception:
                # Fallback: convertir a string simple
                server_config_json = str(self._server_config)
            triggers["server_config"] = server_config_json

        return {
            "resource": {
                "null_resource": {
                    self._name: {
                        "triggers": triggers,
                        "provisioner": [{
                            "local-exec": {
                                "command": (
                                    f"echo 'Creando servidor {self._name} "
                                    f"en subred {self._network.name} "
                                    f"(CIDR {self._network.cidr}, zona {self._zone})'"
                                )
                            }
                        }]
                    }
                }
            }
        }

if __name__ == "__main__":
    # Ejemplo: inyectamos parámetros de configuración del servidor
    sample_config = {
        "display_name": "hello-world-01",
        "tags": {
            "env": "dev",
            "team": "platform"
        }
    }
    Path("main.tf.json").write_text(
        json.dumps(
            ServerFactoryModule("hello-world", server_config=sample_config).resources,
            indent=4,
            sort_keys=True
        )
    )
    print("main.tf.json generado.")
