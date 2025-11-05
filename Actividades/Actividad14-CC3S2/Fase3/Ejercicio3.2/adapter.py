from typing import Dict, Any


class MockBucketAdapter:
	"""Adapter que convierte un bloque `null_resource` a `mock_cloud_bucket`.

	El código acepta varias formas comunes de representar `null_resource` en el
	repositorio y normaliza para obtener la estructura
	name -> {"triggers": {...}} antes de construir el recurso de salida.
	"""

	def __init__(self, null_block: Dict[str, Any]):
		self.null = null_block or {}

	def _extract_mapping(self) -> Dict[str, Dict[str, Any]]:
		"""Extrae un mapping {name: {"triggers": {...}}} a partir del bloque null.

		Maneja formatos como:
		- {"resource": {"null_resource": {"name": {"triggers": {...}}}}}
		- {"resource": [{"null_resource": [{"name": [{"triggers": {...}}]}]}]}
		- variantes anidadas usadas en los ejercicios.
		"""
		res = self.null.get("resource")
		if not res:
			return {}

		# Caso: `resource` es un diccionario con `null_resource` como diccionario.
		if isinstance(res, dict):
			nr = res.get("null_resource")
			if isinstance(nr, dict):
				mapping = {}
				for k, v in nr.items():
					if isinstance(v, dict):
						triggers = v.get("triggers", {})
					else:
						triggers = {}
					mapping[k] = {"triggers": triggers}
				return mapping

		# Caso: `resource` es una lista (común en algunos ejercicios)
		if isinstance(res, list):
			for item in res:
				if not isinstance(item, dict):
					continue
				if "null_resource" not in item:
					continue
				nr = item["null_resource"]
				# nr puede ser una lista o un diccionario.
				if isinstance(nr, dict):
					mapping = {}
					for k, v in nr.items():
						triggers = v.get("triggers", {}) if isinstance(v, dict) else {}
						mapping[k] = {"triggers": triggers}
					return mapping
				if isinstance(nr, list):
					for nr_item in nr:
						if not isinstance(nr_item, dict):
							continue
						for k, v in nr_item.items():
							# v suele ser una lista como [ {"triggers": {...}} ]
							details = None
							if isinstance(v, list) and v:
								details = v[0]
							elif isinstance(v, dict):
								details = v
							triggers = details.get("triggers", {}) if isinstance(details, dict) else {}
							return {k: {"triggers": triggers}}

		# Fallback: Prueba el acceso al diccionario anidado que espera el adaptador de referencia.
		try:
			nr = self.null["resource"]["null_resource"]
			if isinstance(nr, dict):
				mapping = {}
				for k, v in nr.items():
					triggers = v.get("triggers", {}) if isinstance(v, dict) else {}
					mapping[k] = {"triggers": triggers}
				return mapping
		except Exception:
			pass

		return {}

	def to_bucket(self) -> Dict[str, Any]:
		"""Convierte el bloque null a la representación `mock_cloud_bucket`.

		Devuelve un diccionario con la forma:
		{
		  "resource": {
			"mock_cloud_bucket": {
			   "name": {"name": "name", <triggers...>}
			}
		  }
		}
		"""
		mapping = self._extract_mapping()
		if not mapping:
			return {"resource": {"mock_cloud_bucket": {}}}

		# Tomamos el primer recurso disponible
		name = next(iter(mapping))
		triggers = mapping[name].get("triggers", {})

		return {
			"resource": {
				"mock_cloud_bucket": {name: {"name": name, **triggers}}
			}
		}

