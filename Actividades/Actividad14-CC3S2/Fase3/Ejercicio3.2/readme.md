## Ejercicio 3.2: 

#### Prueba: Inserta en builder y exporta un recurso mock_cloud_bucket.

Se han creado 3 archivos con el siguiente funcionamiento:
1. **adapter.py:** Implementa la clase MockBucketAdapter que normaliza distintas formas de representar un bloque null_resource (dict o listas anidadas) y lo convierte a la estructura esperada mock_cloud_bucket (extrae nombre y triggers y los empaqueta en el dict de salida).

2. **builder.py:** Script de demostración que crea un bloque null_resource de ejemplo, usa MockBucketAdapter para transformarlo en mock_cloud_bucket, imprime el JSON resultante y lo escribe en el archivo mock_bucket.tf.json.

3. **test_adapter.py:** Contiene pruebas unitarias que verifican que MockBucketAdapter maneja ambas formas de entrada (forma simple y forma en lista) y un pequeño runner que ejecuta las pruebas cuando se ejecuta el archivo como script.