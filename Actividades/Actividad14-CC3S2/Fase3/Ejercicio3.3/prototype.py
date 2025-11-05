from copy import deepcopy
from typing import Any, Callable, Dict


class ResourcePrototype:
    """Simple implementación de Prototype para recursos representados como dicts.

    - `data` contiene el bloque de recursos (un dict)
    - `clone(mutator)` devuelve un nuevo ResourcePrototype con una copia profunda
      de los datos y aplica la función mutator sobre el dict copiado.
    """

    def __init__(self, template: Dict[str, Any]):
        # Guardamos una copia defensiva
        self.data = deepcopy(template)

    def clone(self, mutator: Callable[[Dict[str, Any]], None] | None = None) -> "ResourcePrototype":
        new_data = deepcopy(self.data)
        if mutator:
            # Mutator modifica el bloque in-place
            mutator(new_data)
        return ResourcePrototype(new_data)
