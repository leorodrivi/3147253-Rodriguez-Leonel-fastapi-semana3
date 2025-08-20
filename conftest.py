import pytest
from fastapi.testclient import TestClient
from main import app
from models import productos_db, Producto
from uuid import uuid4

@pytest.fixture(autouse=True)
def limpiar_base_datos():
    """Fixture para limpiar la base de datos antes de cada test"""
    productos_db.clear()
    yield
    productos_db.clear()

@pytest.fixture
def cliente():
    """Fixture para el cliente de testing"""
    with TestClient(app) as client:
        yield client

@pytest.fixture
def producto_ejemplo():
    """Fixture para crear un producto de ejemplo"""
    return Producto(
        nombre="Laptop Gaming",
        descripcion="Laptop para juegos con RTX 4060",
        precio=1500.99,
        stock=10,
        categoria="Tecnología",
        disponible=True,
        rating=4.5
    )

@pytest.fixture
def producto_ejemplo_2():
    """Fixture para crear un segundo producto de ejemplo"""
    return Producto(
        nombre="Smartphone Samsung",
        descripcion="Teléfono inteligente con 128GB",
        precio=899.99,
        stock=25,
        categoria="Electrónicos",
        disponible=True,
        rating=4.3
    )