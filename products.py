from pydantic import BaseModel, Field, validator
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime

class Producto(BaseModel):
    id: Optional[UUID] = None
    nombre: str = Field(..., min_length=1, max_length=100, example="Laptop Gaming")
    descripcion: Optional[str] = Field(None, max_length=500, example="Laptop para juegos con RTX 4060")
    precio: float = Field(..., gt=0, example=1500.99)
    stock: int = Field(0, ge=0, example=10)
    categoria: str = Field(..., min_length=1, max_length=50, example="Tecnología")
    disponible: bool = Field(True, example=True)
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    rating: float = Field(0.0, ge=0.0, le=5.0, example=4.5)
    
    @validator('nombre')
    def nombre_no_puede_ser_solo_espacios(cls, v):
        """Valida que el nombre no esté vacío o contenga solo espacios"""
        if v.strip() == '':
            raise ValueError('El nombre del producto no puede estar vacío o contener solo espacios')
        return v.title()
    
    @validator('descripcion', pre=True, always=True)
    def descripcion_puede_ser_nula(cls, v):
        """Convierte strings vacíos en None para descripciones opcionales"""
        if v is None or v == "":
            return None
        return v
    
    @validator('precio')
    def precio_debe_ser_positivo(cls, v):
        """Valida que el precio sea positivo"""
        if v <= 0:
            raise ValueError('El precio debe ser mayor a 0')
        return round(v, 2)
    
    @validator('stock')
    def stock_no_puede_ser_negativo(cls, v):
        """Valida que el stock no sea negativo"""
        if v < 0:
            raise ValueError('El stock no puede ser negativo')
        return v

    class Config:
        schema_extra = {
            "example": {
                "nombre": "smartphone samsung",
                "descripcion": "Teléfono inteligente con 128GB de almacenamiento",
                "precio": 899.99,
                "stock": 25,
                "categoria": "Electrónicos",
                "disponible": True,
                "rating": 4.3
            }
        }


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    precio: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    categoria: Optional[str] = Field(None, min_length=1, max_length=50)
    disponible: Optional[bool] = None
    rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    
    @validator('nombre')
    def nombre_no_puede_ser_solo_espacios(cls, v):
        """Valida que el nombre no esté vacío (solo si se proporciona)"""
        if v is not None and v.strip() == '':
            raise ValueError('El nombre no puede estar vacío o contener solo espacios')
        return v.title() if v else v
    
    @validator('precio')
    def precio_debe_ser_positivo(cls, v):
        """Valida que el precio sea positivo"""
        if v is not None and v <= 0:
            raise ValueError('El precio debe ser mayor a 0')
        return round(v, 2) if v else v
    
    @validator('stock')
    def stock_no_puede_ser_negativo(cls, v):
        """Valida que el stock no sea negativo"""
        if v is not None and v < 0:
            raise ValueError('El stock no puede ser negativo')
        return v

productos_db: List[Producto] = []