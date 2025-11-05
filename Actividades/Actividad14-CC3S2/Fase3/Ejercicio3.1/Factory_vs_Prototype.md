
## Factory vs Prototype en IaC

En infraestructura como código (IaC) la elección entre el patrón Factory y el Prototype depende de dos formas principales: la necesidad de estandarización/idempotencia y la necesidad de variación o clonación rápida de configuraciones.

Factory es la opción normal cuando se construyen recursos estandarizados y repetibles. Una fábrica encapsula la lógica de creación (parámetros, validaciones, convenciones), lo que facilita pruebas, control de acceso y cumplimiento. En IaC esto encaja bien con módulos y templates que deben producir recursos idempotentes y previsibles (por ejemplo, módulos de red, instancias base o recursos con políticas uniformes). El coste es que si hay muchas variaciones pequeñas, el código tiende a crecer o a requerir muchas ramas de configuración, lo que aumenta la duplicación y el mantenimiento.

Prototype es mejor cuando necesitas muchas variaciones a partir de una configuración base: clonar un objeto ya configurado y aplicar pequeños cambios es más directo que reconstruirlo desde cero. En IaC puede usarse para acelerar el despliegue de entornos similares (plantillas, imágenes, snapshots) o para generar muchos recursos con configuración base común y pequeñas diferencias.

Costes y rendimiento
- Serializar y clonar (deep copy/serialización profunda) en Prototype suele consumir más memoria y CPU cuando los objetos son grandes (muchos atributos, dependencias o datos incrustados). Para objetos voluminosos la clonación puede implicar IO adicional (snapshots, volcado de estado) y latencias mayores que la creación directa por una Factory.
- Factory normalmente es menos costosa en memoria por instancia y más fácil de optimizar, pero puede implicar trabajo adicional de desarrollo para parametrizar todas las variantes.

Mantenimiento y operabilidad
- Prototype reduce duplicación al permitir basarse en instancias existentes; sin embargo, puede ocultar dependencias implícitas y generar deuda técnica si los clones divergen.
- Factory favorece la claridad, testabilidad e idempotencia: cambios en la lógica de creación se aplican de forma centralizada.

Recomendación:

Usar Factory para recursos estandarizados y cuando la idempotencia, seguridad y trazabilidad son prioritarias. Eligir Prototype cuando los costes de recrear la configuración sean altos y las variaciones sean frecuentes pero debemos medir el coste de serialización/clonación primero. 
Un enfoque híbrido (Factory que produce objetos base y Prototype para variaciones puntuales) suele ofrecer el mejor equilibrio.

Ejemplos en este casi serian: `Fase2/Ejercicio2.2/factory.py` y `Fase2/Ejercicio2.3/prototype.py`.

