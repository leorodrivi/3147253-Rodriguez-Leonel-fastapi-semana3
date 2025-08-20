import time
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from models import Producto

def simular_retraso_db():
    """Simula un pequeño retraso de base de datos"""
    time.sleep(0.1)

def generar_timestamps() -> dict:
    """Genera timestamps de creación y actualización"""
    ahora = datetime.now()
    return {
        "fecha_creacion": ahora,
        "fecha_actualizacion": ahora
    }

def actualizar_timestamp() -> datetime:
    """Retorna el timestamp actual para actualizaciones"""
    return datetime.now()

def filtrar_productos(
    productos: List[Producto],
    disponible: Optional[bool] = None,
    categoria: Optional[str] = None,
    precio_max: Optional[float] = None
) -> List[Producto]:
    """Filtra productos según los criterios especificados"""
    productos_filtrados = productos
    
    if disponible is not None:
        productos_filtrados = [p for p in productos_filtrados if p.disponible == disponible]
        
    if categoria:
        categoria_lower = categoria.lower()
        productos_filtrados = [p for p in productos_filtrados if p.categoria.lower() == categoria_lower]
    
    if precio_max is not None:
        if precio_max <= 0:
            from exceptions import PrecioInvalidoError
            raise PrecioInvalidoError("El precio máximo debe ser mayor a 0")
        productos_filtrados = [p for p in productos_filtrados if p.precio <= precio_max]
    
    return productos_filtrados

def buscar_productos_por_texto(
    productos: List[Producto],
    query: str,
    min_rating: Optional[float] = None
) -> List[Producto]:
    """Busca productos por texto en nombre o descripción"""
    if len(query.strip()) < 2:
        from exceptions import BusquedaInvalidaError
        raise BusquedaInvalidaError("El término de búsqueda debe tener al menos 2 caracteres")
    
    query_lower = query.lower()
    resultados = []
    
    for producto in productos:
        if (query_lower in producto.nombre.lower() or 
            (producto.descripcion and query_lower in producto.descripcion.lower())):
            
            if min_rating is None or producto.rating >= min_rating:
                resultados.append(producto)
    
    return resultados

def verificar_producto_duplicado(
    productos: List[Producto],
    nombre: str,
    exclude_id: Optional[UUID] = None
) -> bool:
    """Verifica si ya existe un producto con el mismo nombre"""
    nombre_lower = nombre.lower()
    for producto in productos:
        if producto.nombre.lower() == nombre_lower:
            if exclude_id is None or producto.id != exclude_id:
                return True
    return False