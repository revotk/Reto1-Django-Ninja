from ninja import Schema

class UsuarioSchema(Schema):
    id: int
    nombre: str
    apellido_paterno: str
    apellido_materno: str
    edad: int
    nombre_cuenta: str
    contraseña: str

class UsuarioCreateSchema(Schema):
    nombre: str
    apellido_paterno: str
    apellido_materno: str
    edad: int
    nombre_cuenta: str
    contraseña: str
