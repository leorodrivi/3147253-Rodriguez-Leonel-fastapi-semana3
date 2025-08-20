import pytest
from uuid import UUID, uuid4
from fastapi import status
from models import Producto

def test_crear_producto(cliente, producto_ejemplo):
    """Test para crear un producto"""
    response = cliente.post("/productos", json=producto_ejemplo.dict())
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["nombre"] == "Laptop Gaming"
    assert UUID(response.json()["id"])

def test_obtener_producto_no_existente(cliente):
    """Test para obtener un producto que no existe"""
    producto_id = uuid4()
    response = cliente.get(f"/productos/{producto_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_obtener_todos_los_productos(cliente, producto_ejemplo, producto_ejemplo_2):
    """Test para obtener todos los productos"""
    cliente.post("/productos", json=producto_ejemplo.dict())
    cliente.post("/productos", json=producto_ejemplo_2.dict())

    response = cliente.get("/productos")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2

def test_actualizar_producto(cliente, producto_ejemplo):
    """Test para actualizar un producto"""
    crear_response = cliente.post("/productos", json=producto_ejemplo.dict())
    producto_id = crear_response.json()["id"]

    update_data = {"precio": 1299.99, "stock": 15}
    response = cliente.put(f"/productos/{producto_id}", json=update_data)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["precio"] == 1299.99
    assert response.json()["stock"] == 15

def test_eliminar_producto(cliente, producto_ejemplo):
    """Test para eliminar un producto"""
    crear_response = cliente.post("/productos", json=producto_ejemplo.dict())
    producto_id = crear_response.json()["id"]

    response = cliente.delete(f"/productos/{producto_id}")
    assert response.status_code == status.HTTP_200_OK

    get_response = cliente.get(f"/productos/{producto_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_buscar_productos(cliente, producto_ejemplo, producto_ejemplo_2):
    """Test para buscar productos"""
    cliente.post("/productos", json=producto_ejemplo.dict())
    cliente.post("/productos", json=producto_ejemplo_2.dict())

    response = cliente.get("/productos/buscar?q=gaming")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]["nombre"] == "Laptop Gaming"