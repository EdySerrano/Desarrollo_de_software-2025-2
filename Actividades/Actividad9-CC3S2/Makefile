VENV=.venv
PYTHON := $(shell command -v python3 2>/dev/null || command -v python 2>/dev/null || echo python3)
PY=$(VENV)/bin/python
PIP=$(VENV)/bin/pip
PYTEST=$(VENV)/bin/pytest

.PHONY: venv deps test_all test_unit cov clean

venv:
	$(PYTHON) -m venv $(VENV)

deps: venv
	$(PIP) install -r requirements.txt

# Ejecuta pytest en cada sub-actividad
test_all:
	cd soluciones/aserciones_pruebas   && ../../$(PYTEST) -q || exit 1
	cd soluciones/pruebas_pytest       && ../../$(PYTEST) -q || exit 1
	cd soluciones/pruebas_fixtures     && ../../$(PYTEST) -q || exit 1
	cd soluciones/coverage_pruebas     && ../../$(PYTEST) --cov=models --cov-report term-missing -q || exit 1
	cd soluciones/factories_fakes      && ../../$(PYTEST) -q || exit 1
	cd soluciones/mocking_objetos      && ../../$(PYTEST) -q || exit 1
	cd soluciones/practica_tdd         && ../../$(PYTEST) -q || exit 1

# Atajo para correr sólo unidad si decides marcar tests con -m "unit"
test_unit:
	cd soluciones && ../$(PYTEST) -m "unit" -q

# Cobertura sólo para coverage_pruebas (puedes extender a otras)
cov:
	cd soluciones/coverage_pruebas && ../../$(PYTEST) --cov=models --cov-report term-missing -q

# Cobertura individual con reporte HTML detallado
coverage_individual:
	cd soluciones/coverage_pruebas && ../../$(PYTEST) --cov=models --cov-report=html --cov-report=term-missing -v

clean:
	rm -rf .pytest_cache **/__pycache__ htmlcov .coverage