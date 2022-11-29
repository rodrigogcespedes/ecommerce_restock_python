from fastapi import FastAPI
from Entities import OrdenRestockCompleta
from Entities import OrdenRestockVacia
from Entities import ArticuloVacio
from Entities import ArticuloModificacion
from services.articulo_service import crear_articulo, modificar_articulo, buscar_un_articulo, borrar_articulo
from services.orden_service import crear_orden, finalizar_orden, cancelar_orden, buscar_ordenes_pendintes, buscar_ordenes_por_articulo, buscar_una_orden

# python -m uvicorn server:app --port 9600 --reload

app = FastAPI()


@app.get('/{idOrdenRestock}/ordenRestock')
def load(idOrdenRestock: str):
    return buscar_una_orden(idOrdenRestock)


@app.get('/ordenesPendientes')
def load():
    return buscar_ordenes_pendintes()


@app.get('/{idArticulo}/ordenesPorArticulo')
def load(idArticulo: str):
    return buscar_ordenes_por_articulo(idArticulo)


@app.put('/{idOrdenRestock}/cancelarOrden')
def load(idOrdenRestock: str):
    return cancelar_orden(idOrdenRestock)


@app.put('/{idOrdenRestock}/finalizarOrden')
def load(idOrdenRestock: str):
    return finalizar_orden(idOrdenRestock)


@app.post('/crearOrden')
def load(body: OrdenRestockVacia):
    return crear_orden(body.__dict__)


@app.post('/crearArticulo')
def load(body: ArticuloVacio):
    return crear_articulo(body.__dict__)


@app.put('/{idArticulo}/modificarArticulo')
def load(idArticulo: str, body: ArticuloModificacion):
    return modificar_articulo(idArticulo, body.__dict__)


@app.delete('/{idArticulo}/borrarArticulo')
def load(idArticulo: str):
    return borrar_articulo(idArticulo)
