"""Pequeño builder de prueba para usar MockBucketAdapter.

Este script crea un bloque `null_resource` en la forma simple que el
adapter acepta, lo convierte a `mock_cloud_bucket` y escribe
`mock_bucket.tf.json` con el recurso exportado.
"""
import json
from adapter import MockBucketAdapter


def build_and_export():
    # Creamos un bloque null en la forma simple (dict) para la demo.
    null_block = {
        "resource": {
            "null_resource": {
                "app_bucket": {
                    "triggers": {
                        "owner": "team-a",
                        "env": "dev",
                    }
                }
            }
        }
    }

    adapter = MockBucketAdapter(null_block)
    bucket = adapter.to_bucket()

    # Imprimir a stdout y volcar a archivo
    print(json.dumps(bucket, indent=2, ensure_ascii=False))
    with open("mock_bucket.tf.json", "w", encoding="utf-8") as f:
        json.dump(bucket, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    build_and_export()
