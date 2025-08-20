from fastapi import FastAPI, HTTPException, status
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
import time
from products import Producto, ProductoUpdate, productos_db

app = FastAPI(
    title="API de Productos - Tienda Online",
    description="API para gestión de productos de una tienda online",
    version="1.0.0"
)

def simular_retraso_db():
    """Simula un pequeño retraso de base de datos"""
    time.sleep(0.1)

@app.middleware("http")
async def manejar_tiempo_solicitud(request, call_next):
    """Middleware para medir el tiempo de procesamiento de solicitudes"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/")
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "Bienvenido a la API de Productos",
        "version": "1.0.0",
        "endpoints": {
            "Obtener todos los productos": "GET /productos",
            "Obtener un producto": "GET /productos/{id}",
            "Crear producto": "POST /productos",
            "Actualizar producto": "PUT /productos/{id}",
            "Eliminar producto": "DELETE /productos/{id}",
            "Buscar productos": "GET /productos/buscar"
        }
    }

@app.get("/productos", response_model=List[Producto], status_code=status.HTTP_200_OK)
async def obtener_todos_los_productos(
    disponible: Optional[bool] = None, 
    categoria: Optional[str] = None,
    precio_max: Optional[float] = None
):
    """Obtiene todos los productos, con filtros opcionales"""
    try:
        simular_retraso_db()
        
        productos_filtrados = productos_db
        
        if disponible is not None:
            productos_filtrados = [p for p in productos_filtrados if p.disponible == disponible]
            
        if categoria:
            categoria_lower = categoria.lower()
            productos_filtrados = [p for p in productos_filtrados if p.categoria.lower() == categoria_lower]
        
        if precio_max is not None:
            if precio_max <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El precio máximo debe ser mayor a 0"
                )
            productos_filtrados = [p for p in productos_filtrados if p.precio <= precio_max]
        
        return productos_filtrados
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@app.get("/productos/{producto_id}", response_model=Producto, status_code=status.HTTP_200_OK)
async def obtener_producto(producto_id: UUID):
    """Obtiene un producto específico por su ID."""
    try:
        simular_retraso_db()
        
        for producto in productos_db:
            if producto.id == producto_id:
                return producto
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@app.post("/productos", response_model=Producto, status_code=status.HTTP_201_CREATED)
async def crear_producto(producto: Producto):
    """Crea un nuevo producto."""
    try:
        simular_retraso_db()

        producto.id = uuid4()
        ahora = datetime.now()
        producto.fecha_creacion = ahora
        producto.fecha_actualizacion = ahora

        for producto_existente in productos_db:
            if producto_existente.nombre.lower() == producto.nombre.lower():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe un producto con ese nombre"
                )

        productos_db.append(producto)
        
        return producto
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@app.put("/productos/{producto_id}", response_model=Producto, status_code=status.HTTP_200_OK)
async def actualizar_producto(producto_id: UUID, producto_actualizado: ProductoUpdate):
    """Actualiza un producto existente."""
    try:
        simular_retraso_db()

        producto_encontrado = None
        for producto in productos_db:
            if producto.id == producto_id:
                producto_encontrado = producto
                break
        
        if not producto_encontrado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {producto_id} no encontrado"
            )

        if producto_actualizado.nombre is not None:
            for producto_existente in productos_db:
                if (producto_existente.id != producto_id and 
                    producto_existente.nombre.lower() == producto_actualizado.nombre.lower()):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Ya existe un producto con ese nombre"
                    )

        update_data = producto_actualizado.dict(exclude_unset=True)
        for campo, valor in update_data.items():
            if valor is not None:
                setattr(producto_encontrado, campo, valor)

        producto_encontrado.fecha_actualizacion = datetime.now()
        
        return producto_encontrado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@app.delete("/productos/{producto_id}", status_code=status.HTTP_200_OK)
async def eliminar_producto(producto_id: UUID):
    """Elimina un producto existente."""
    try:
        simular_retraso_db()

        for i, producto in enumerate(productos_db):
            if producto.id == producto_id:
                producto_eliminado = productos_db.pop(i)
                return {
                    "message": "Producto eliminado correctamente",
                    "producto_eliminado": producto_eliminado
                }
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@app.get("/productos/buscar", response_model=List[Producto])
async def buscar_productos(q: str, min_rating: Optional[float] = None):
    """Busca productos por término en nombre o descripción"""
    try:
        if len(q.strip()) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El término de búsqueda debe tener al menos 2 caracteres"
            )
        
        q_lower = q.lower()
        resultados = []
        
        for producto in productos_db:
            if (q_lower in producto.nombre.lower() or 
                (producto.descripcion and q_lower in producto.descripcion.lower())):
                
                if min_rating is None or producto.rating >= min_rating:
                    resultados.append(producto)
        
        return resultados
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la búsqueda: {str(e)}"
        )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Manejador global de excepciones HTTP"""
    return {
        "error": {
            "message": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat()
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)