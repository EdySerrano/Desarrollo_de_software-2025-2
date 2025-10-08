"""
Casos de prueba para Mocking Lab
"""
import os
import json
import pytest
import sys

# Agregar el directorio raíz al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch, Mock
from requests import Response
from models.imdb import IMDb

# Variable global para los datos de IMDb
IMDB_DATA = {}

# Fixture para cargar los datos de IMDb desde un archivo JSON
@pytest.fixture(scope="session", autouse=True)
def load_imdb_data():
    """Carga las respuestas de IMDb necesarias para las pruebas"""
    global IMDB_DATA
    current_dir = os.path.dirname(__file__)
    fixture_path = os.path.join(current_dir, 'fixtures', 'imdb_responses.json')
    with open(fixture_path) as json_data:
        IMDB_DATA = json.load(json_data)


class TestIMDbDatabase:
    """Casos de prueba para la base de datos de IMDb"""

    # Paso 1: Prueba de búsqueda por título exitosa
    @patch('models.imdb.requests.get')
    def test_search_by_title(self, imdb_mock):
        """Prueba de búsqueda por título"""
        imdb_mock.return_value = Mock(
            spec=Response,
            status_code=200,
            json=Mock(return_value=IMDB_DATA["search_title"])
        )
        imdb = IMDb("k_12345678")
        resultados = imdb.search_titles("Bambi")
        assert resultados is not None
        assert resultados.get("errorMessage") is None
        assert resultados.get("results") is not None
        assert resultados["results"][0]["id"] == "tt1375666"

    # Paso 2: Búsqueda sin resultados (usando patch en requests.get)
    @patch('models.imdb.requests.get')
    def test_search_with_no_results(self, imdb_mock):
        """Prueba de búsqueda sin resultados"""
        imdb_mock.return_value = Mock(status_code=404)
        imdb = IMDb("k_12345678")
        resultados = imdb.search_titles("TituloInexistente")
        assert resultados == {}

    # Paso 3: Búsqueda por título fallida (API key inválida)
    @patch('models.imdb.requests.get')
    def test_search_by_title_failed(self, imdb_mock):
        """Prueba de búsqueda por título fallida"""
        imdb_mock.return_value = Mock(
            spec=Response,
            status_code=200,
            json=Mock(return_value=IMDB_DATA["INVALID_API"])
        )
        imdb = IMDb("bad-key")
        resultados = imdb.search_titles("Bambi")
        assert resultados is not None
        assert resultados["errorMessage"] == "Invalid API Key"

    # Paso 4: Prueba de calificaciones de películas
    @patch('models.imdb.requests.get')
    def test_movie_ratings(self, imdb_mock):
        """Prueba de calificaciones de películas"""
        imdb_mock.return_value = Mock(
            spec=Response,
            status_code=200,
            json=Mock(return_value=IMDB_DATA["GOOD_RATING"])
        )
        imdb = IMDb("k_12345678")
        resultados = imdb.movie_ratings("tt1375666")
        assert resultados is not None
        assert resultados["title"] == "Bambi"
        assert resultados["filmAffinity"] == 3
        assert resultados["rottenTomatoes"] == 5

    # Tests adicionales para completar la cobertura

    @patch('models.imdb.requests.get')
    def test_movie_reviews_success(self, imdb_mock):
        """Prueba de reseñas de películas exitosa"""
        imdb_mock.return_value = Mock(
            spec=Response,
            status_code=200,
            json=Mock(return_value=IMDB_DATA["movie_reviews"])
        )
        imdb = IMDb("k_12345678")
        resultados = imdb.movie_reviews("tt1375666")
        assert resultados is not None
        assert resultados["title"] == "Bambi"
        assert resultados["imDbId"] == "tt1375666"
        assert len(resultados["items"]) > 0

    @patch('models.imdb.requests.get')
    def test_movie_reviews_failure(self, imdb_mock):
        """Prueba de reseñas de películas fallida"""
        imdb_mock.return_value = Mock(status_code=404)
        imdb = IMDb("k_12345678")
        resultados = imdb.movie_reviews("invalid_id")
        assert resultados == {}

    @patch('models.imdb.requests.get')
    def test_movie_ratings_failure(self, imdb_mock):
        """Prueba de calificaciones de películas fallida"""
        imdb_mock.return_value = Mock(status_code=500)
        imdb = IMDb("k_12345678")
        resultados = imdb.movie_ratings("invalid_id")
        assert resultados == {}
