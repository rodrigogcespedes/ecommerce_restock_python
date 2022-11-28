from pydantic import BaseModel


class OrdenRestockCompleta(BaseModel):
    fechaEmision: str
    estado: str
    idArticulo: str
    cantidad: int


class OrdenRestockVacia(BaseModel):
    idArticulo: str
    cantidad: int


class ArticuloModificacion(BaseModel):
    umbral: int
    cantidadRestock: int
    altaDemanda: bool
    noReponer: bool


class ArticuloVacio(BaseModel):
    idArticulo: str
    umbral: int
    cantidadRestock: int
    altaDemanda: bool
    noReponer: bool
