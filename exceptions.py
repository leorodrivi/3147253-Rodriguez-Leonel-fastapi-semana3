class ProductoNoEncontradoError(Exception):
    """Excepción cuando un producto no existe"""
    pass

class ProductoDuplicadoError(Exception):
    """Excepción cuando ya existe un producto con el mismo nombre"""
    pass

class PrecioInvalidoError(Exception):
    """Excepción cuando el precio es inválido"""
    pass

class StockNegativoError(Exception):
    """Excepción cuando el stock es negativo"""
    pass

class BusquedaInvalidaError(Exception):
    """Excepción cuando la búsqueda es inválida"""
    pass