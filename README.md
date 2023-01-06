## Microservicio de Reposicion de Stock

Para correr el servicio:

* Puede clonar el proyecto y ejecutar desde el directorio principal ```pip install --no-cache-dir -r requirements.txt``` y luego ```python -m uvicorn server:app --port 9600 --reload```
* Tambien se puede correr con una imagen de docker, construyala clonando el proyecto y ejecutado la instruccion ```docker image build -t restock_service .``` y luego ```docker run -it -p 9600:9600 restock_service```
* Tambien se puede descargar la imagen ya construida desde DockerHub con la instruccion ```docker run -it -p 9600:9600 rodrigogcespedes/restock_service:0.1```

### Casos de uso

![alt text](https://www.plantuml.com/plantuml/png/TSwz2i8m40VmlKznPDAXWssd8gLHSEiY-0176YHuII2vB3wzeQqjY5r2kDzz_Fl863XPAjf7rA65ikpWaB-d8xGWpgOJlrBjIhqhpIRYhYDxzO81NK8IW74vM8WhEgK90omzArOPRyOXcVSVhRFAom0oi569_0hDj9EH_7Ckoj4QLqpldEqRHYRs5lEutvBsset9qWS0)

#### CU Restock Automatico
**Descripcion:** Cuando el stock de un articulo disminuye, se genera una Orden de Restock automáticamente si es necesario.

**Precondicion:** Debe existir un Articulo en la base de datos del microservicio con los atributos.
* id: string
* idAtributo: string
* umbral: int
* cantidadRestock: int
* noReponer: bool
* altaDemanda: bool
* ultimaOrden: string

**Camino normal:**
1. Cuando cambia el stock de un articulo, se controla si el nuevo stock esta por debajo del valor del umbral (si altaDemanda es False) o por debajo del doble del valor del umbral (si altaDemanda es True).
2. Si ese es el caso, se revisa que la bandera noReponer sea False.
3. Se controla que la orden referenciada por el atributo ultimaOrden tenga un valor distinto a "pendiente" en su atributo estado.
4. Se crea una Orden de Restock de tantos articulos como figure en el atributo cantidadRestock.
5. Se setea en atributo ultimaOrden del Articulo, el id de la orden creada.
6. Se publica un mensaje con el id de la orden de restock, el id del articulo y la cantidad del mismo para que sea leido por el microservicio Proveedores para gestionar la compra y el microservicio de Mailing para que se notifique a los administradores de la Orden de Restock creada.

**Camino alternativo 1: El stock actual del articulo es mayor a lo especificado por los atributos umbral y altaDemanda.**

2. No se genera ninguna Orden de Restock ni se modifica ninguna valor en el microservicio.

**Camino alternativo 2: La bandera noReponer es True.**

3. Significa que ese articulo no debe reponerse, por lo que no se genera ninguna Orden de Restock ni se modifica ninguna valor en el microservicio.

**Camino alternativo 3: Se encentra una Orden de Restock que tiene asignado el valor "pendiente" en su atributo estado.**

4. Significa que ya hay una Orden de Restock activa para este articulo, por lo que no se genera ninguna Orden de Restock ni se modifica ninguna valor en el microservicio.

**Camino alternativo 4: El atributo ultimaOrden tiene el valor string "0".**
Este es el valor con el que se crean las entidades de Atributo, significa que no se ha generado ninguna orden aun.

4. Se crea una Orden de Restock de tantos articulos como figure en el atributo cantidadRestock.

5. Se setea en atributo ultimaOrden del Articulo, el id de la orden creada.

6. Se publica en un mensaje con el id de la orden de restock, el id del articulo y la cantidad del mismo para que sea leido por el microservicio Proveedores para gestionar la compra y el microservicio de Mailing para que se notifique a los administradores de la Orden de Restock creada.


#### CU Restock Manual
**Descripcion:** Un usuario crea una Orden de Restock manualmente.

**Precondicion:** Debe existir un Articulo en la base de datos del microservicio con los atributos.
* id: string
* idAtributo: string
* umbral: int
* cantidadRestock: int
* noReponer: bool
* altaDemanda: bool
* ultimaOrden: string

**Camino normal:**
1. Se envía una solicitud con el id del articulo y la cantidad a reponer.
2. Se crea una nueva Orden de Restock con estado "pendiente" de tantos articulos como haya elegido el usuario.
3. Se setea en atributo ultimaOrden del Articulo, el id de la orden creada.
4. Se publica en un mensaje con el id de la orden de restock, el id del articulo y la cantidad del mismo para que sea leido por el microservicio Proveedores para gestionar la compra y el microservicio de Mailing para que se notifique a los administradores de la Orden de Restock creada.


#### CU ABM Articulo
**Descripcion:**
* Alta: Se crea un articulo con el id provisto por el microservicio de Catalogo, y el atributo ultimaOrden con la cadena "0". Los demas atributos son provistos por el usuario durante la creacion.
* Baja y modificacion: Se pueden modificar los atributos: umbral, cantidadRestock, altaDemanda, noReponer (se entiende que si este es True, para el microservicio de Restock, el articulo esta dado de baja).
* Consulta: Se puede consultar el estado de todos los Articulos o el de un Articulo en especifico si se provee su id.


#### CU Cancelar Orden de Restock
**Descripcion:** Se cancela una Orden de Restock.

**Camino normal:**
1. Se ingresa el id de la Orden de Restock.
2. Si la Orden de Restock existe y se encuentra con estado "pendiente", se le asigna el estado "cancelada".
3. Se publica un mensaje con el id de la orden de restock, el id del articulo y la cantidad del mismo.

**Camino alternativo 1: El id ingresado no se corresponde con el de una Orden de Restock.**

2. Se retorna un mensaje indicando que el id ingresado no corresponde a una Orden de Restock.

**Camino alternativo 2: La Orden de Restock tiene un estado distinto de "pendiente".**

2. Se retorna un mensaje indicando que el id ingresado no corresponde a una Orden de Restock.


#### CU Finalizar Orden de Restock
**Descripcion:** Se indica que una Orden de Restock concluyo exitosamente.

**Camino normal:**
1. Se ingresa el id de la Orden de Restock.
2. Si la Orden de Restock existe y se encuentra con estado "pendiente", se le asigna el estado "finalizada".
3. Se publica un mensaje con el id de la orden de restock, el id del articulo y la cantidad del mismo.

**Camino alternativo 1: El id ingresado no se corresponde con el de una Orden de Restock.**

2. Se retorna un mensaje indicando que el id ingresado no corresponde a una Orden de Restock.

**Camino alternativo 2: La Orden de Restock tiene un estado distinto de "pendiente".**

2. Se retorna un mensaje indicando que el id ingresado no corresponde a una Orden de Restock.


### Modelo de datos

**Articulo**
```json
{
    "id" : "string",
    "idArticulo" : "string",
    "umbral" : "int",
    "cantidadRestock" : "int",
    "altaDemanda" : "bool",
    "noReponer" : "bool",
    "ultimaOrden" : "string"
}
```

**OrdenRestock**
```json
{
    "id" : "string",
    "idArticulo" : "string",
    "fechaEmision" : "date",
    "cantidad" : "int",
    "estado" : "string"
}
```
> Estado puede tomar los valores "pendiente", "finalizada" o cancelada".


### Interfaz REST

**Cancelar Orden de Restock**

`PUT /{idOrdenRestock}/cancelarOrden`

Body
```json
{}
```
Response `200 OK`

```json
{
    "id" : "string",
    "idArticulo" : "string",
    "fechaEmision" : "date",
    "cantidad" : "int",
    "estado" : "cancelada"
}
```


**Finalizar Orden de Restock**

`PUT /{idOrdenRestock}/finalizarOrden`

Body
```json
{}
```
Response `200 OK`
```json
{
    "id" : "string",
    "idArticulo" : "string",
    "fechaEmision" : "date",
    "cantidad" : "int",
    "estado" : "finalizada"
}
```


**Consultar Orden de Restock**

`GET /{idOrdenRestock}/ordenRestock`

Response `200 OK`
```json
{
    "id" : "string",
    "idArticulo" : "string",
    "fechaEmision" : "date",
    "cantidad" : "int",
    "estado" : "string"
}
```


**Consultar Ordenes de Restock pedientes**

`GET /ordenesPendientes`

Response `200 OK`
```json
{
	"ordenes": [
	{
	    "id" : "string",
	    "idArticulo" : "string",
	    "fechaEmision" : "date",
	    "cantidad" : "int",
	    "estado" : "pendiente"
    }]	
}
```


**Consultar Ordenes de Restock de un Articulo**

`GET /{idArticulo}/ordenesPorArticulo`

Response `200 OK`
```json
{
    "id" : "string",
    "idArticulo" : "string",
    "umbral" : "int",
    "cantidadRestock" : "int",
    "altaDemanda" : "bool",
    "noReponer" : "bool",
    "ultimaOrden" : "string",
	"ordenes": [
	{
	    "id" : "string",
	    "idArticulo" : "string",
	    "fechaEmision" : "date",
	    "cantidad" : "int",
	    "estado" : "pendiente"
    }]	
}
```


**Crear Orden de Restock Manualmente**

`POST /crearOrden`

Body
```json
{
    "idArticulo" : "string",
    "cantidad" : "int"
}
```
Response `201 Created`
```json
{
    "id" : "string",
    "idArticulo" : "string",
    "fechaEmision" : "date",
    "cantidad" : "int",
    "estado" : "finalizada"
}
```


**Crear Articulo**

`POST /crearArticulo`

Body
```json
{
    "idArticulo" : "string",
    "umbral" : "int",
    "cantidadRestock" : "int",
    "altaDemanda" : "bool",
    "noReponer" : "bool"
}
```
Response `201 Created`
```json
{
    "id" : "string",
    "idArticulo" : "string",
    "umbral" : "int",
    "cantidadRestock" : "int",
    "altaDemanda" : "bool",
    "noReponer" : "bool",
    "ultimaOrden" : "0"
}
```


**Modificar Articulo**

`PUT /{idArticulo}/modificarArticulo`

Body
```json
{
    "umbral" : "int",
    "cantidadRestock" : "int",
    "altaDemanda" : "bool",
    "noReponer" : "bool"
}
```
Response `200 OK`
```json
{
    "id" : "string",
    "idArticulo" : "string",
    "umbral" : "int",
    "cantidadRestock" : "int",
    "altaDemanda" : "bool",
    "noReponer" : "bool",
    "ultimaOrden" : "string"
}
```


**Borrar Articulo**

`DELETE /{idArticulo}/borrarArticulo`

Response `200 OK`
```json
{
    "id" : "string",
    "idArticulo" : "string",
    "umbral" : "int",
    "cantidadRestock" : "int",
    "altaDemanda" : "bool",
    "noReponer" : "True",
    "ultimaOrden" : "string"
}
```


### Interfaz asincronica (RabbitMQ)

Se crea el exchange `Restock` de tipo `topic` para que sea consultado por los microservicios que necesiten saber sobre las Ordenes de Restock.

> Los topicos previstos son "order.created", "order.canceled" y "order.finished".

**Control de Restock Automatico**

Recibe el id y el stock de un articulo del microservicio Catalogo

Body
```json
{
    "idArticulo" : "string",
    "cantidad" : "int"
}
```


**Creacion de Orden de Restock**

Publica en el exchange `Restock` con `routing_key = "order.created"`

Body
```json
{
    "idOrdenRestock": "string",
    "idArticulo" : "string",
    "cantidad" : "int"
}
```


**Cancelacion de Orden de Restock**

Publica en el exchange `Restock` con `routing_key = "order.canceled"`

Body
```json
{
    "idOrdenRestock": "string",
    "idArticulo" : "string",
    "cantidad" : "int"
}
```


**Finalizacion de Orden de Restock**

Publica en el exchange `Restock` con `routing_key = "order.finished"`

Body
```json
{
    "idOrdenRestock": "string",
    "idArticulo" : "string",
    "cantidad" : "int"
}
```
