from pydantic import BaseModel, Field, validator
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime

class Tarea(BaseModel):
    id: Optional[UUID] = None
    titulo: str = Field(..., min_length=1, max_length=100, example="Comprar leche")
    descripcion: Optional[str] = Field(None, max_length=500, example="Ir al supermercado")
    completada: bool = Field(False, example=False)
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    prioridad: int = Field(1, ge=1, le=5, example=3)
    
    @validator('titulo')
    def titulo_no_puede_ser_solo_espacios(cls, v):
        """Valida que el título no esté vacío o contenga solo espacios"""
        if v.strip() == '':
            raise ValueError('El título no puede estar vacío o contener solo espacios')
        return v
    
    @validator('descripcion', pre=True, always=True)
    def descripcion_puede_ser_nula(cls, v):
        """Convierte strings vacíos en None para descripciones opcionales"""
        if v is None or v == "":
            return None
        return v

    class Config:
        schema_extra = {
            "example": {
                "titulo": "Estudiar FastAPI",
                "descripcion": "Completar los ejercicios de la semana 3",
                "completada": False,
                "prioridad": 4
            }
        }


class TareaUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    completada: Optional[bool] = None
    prioridad: Optional[int] = Field(None, ge=1, le=5)
    
    @validator('titulo')
    def titulo_no_puede_ser_solo_espacios(cls, v):
        """Valida que el título no esté vacío (solo si se proporciona)"""
        if v is not None and v.strip() == '':
            raise ValueError('El título no puede estar vacío o contener solo espacios')
        return v


tareas_db: List[Tarea] = []