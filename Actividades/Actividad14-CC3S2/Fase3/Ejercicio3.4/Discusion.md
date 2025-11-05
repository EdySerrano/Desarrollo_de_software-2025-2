### Escalabilidad de JSON y su impacto en CI/CD

Generar un único `main.tf.json` con muchos recursos (ej. 15 vs 150) tiene efectos prácticos en pipelines y repositorios. A medida que el fichero crece, el tiempo de parsing y la memoria requerida por herramientas (linters, validadores, el propio Terraform en sus operaciones de planificación) aumenta aproximadamente de forma lineal con el tamaño del archivo; en CI esto se traduce en jobs más lentos y mayores picos de uso de memoria en runners. Además, archivos grandes generan diffs voluminosos que encarecen revisiones y aumentan el tamaño del repositorio (y de sus clones), lo que puede impactar en límites de almacenamiento o en el tiempo de checkout en CI. Los logs y artefactos también crecen, y algunos servicios de CI/SCM imponen límites por archivo o por repositorio que conviene vigilar.

Estrategias de fragmentación y mitigación

- Modularizar: dividir la infraestructura en módulos Terraform independientes (por componente o por capas) reduce el tamaño de cada archivo y permite validar y aplicar módulos por separado.
- Evitar JSON generados cuando no sea necesario: usar HCL directo suele producir ficheros más legibles y compactos; además, HCL es el formato nativo de Terraform y su tooling puede ser más eficiente.
- Herramientas de orquestación: Terragrunt o soluciones similares permiten componer y reutilizar configuraciones, manejar backends remotos y ejecutar en paralelo subconjuntos de infraestructura.
- No versionar artefactos generados: mantener los `*.tf.json` generados fuera del control de versiones y almacenar artefactos en un bucket o registry para CI evita inflar el repo.
- Particionado lógico: generar varios JSON por funcionalidad o por rango (por ejemplo: main_0-49.tf.json, main_50-99.tf.json) para paralelizar validaciones y aplicar sólo lo necesario.

