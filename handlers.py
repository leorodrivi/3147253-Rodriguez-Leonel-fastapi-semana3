from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from datetime import datetime
from exceptions import *

async def http_exception_handler(request: Request, exc: HTTPException):
    """Manejador global de excepciones HTTP"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.detail,
                "status_code": exc.status_code,
                "timestamp": datetime.now().isoformat(),
                "path": request.url.path
            }
        }
    )

async def producto_no_encontrado_handler(request: Request, exc: ProductoNoEncontradoError):
    """Manejador para producto no encontrado"""
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "message": str(exc),
                "error_code": "PRODUCTO_NO_ENCONTRADO",
                "timestamp": datetime.now().isoformat()
            }
        }
    )

async def producto_duplicado_handler(request: Request, exc: ProductoDuplicadoError):
    """Manejador para producto duplicado"""
    return JSONResponse(
        status_code=409,
        content={
            "error": {
                "message": str(exc),
                "error_code": "PRODUCTO_DUPLICADO",
                "timestamp": datetime.now().isoformat()
            }
        }
    )

async def precio_invalido_handler(request: Request, exc: PrecioInvalidoError):
    """Manejador para precio inválido"""
    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "message": str(exc),
                "error_code": "PRECIO_INVALIDO",
                "timestamp": datetime.now().isoformat()
            }
        }
    )

async def busqueda_invalida_handler(request: Request, exc: BusquedaInvalidaError):
    """Manejador para búsqueda inválida"""
    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "message": str(exc),
                "error_code": "BUSQUEDA_INVALIDA",
                "timestamp": datetime.now().isoformat()
            }
        }
    )