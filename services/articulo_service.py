from repositories.articulo_repository import buscar_uno, crear, modificar, borrar
from Entities import OrdenRestockVacia
from Entities import ArticuloVacio
from Entities import ArticuloModificacion


def buscar_un_articulo(id: str):
    articulo = buscar_uno(id)
    del articulo['_id']
    return articulo


def crear_articulo(body: dict):
    articulo_nuevo = crear(body)
    return articulo_nuevo


def modificar_articulo(idArticulo: str, body: dict):
    articulo_modificado = modificar(idArticulo, body)
    return articulo_modificado


def borrar_articulo(idArticulo: str):
    articulo_borrado = borrar(idArticulo)
    return articulo_borrado
