from ninja import NinjaAPI
from ninja.errors import HttpError
from .models import Usuario
from .schemas import UsuarioSchema, UsuarioCreateSchema
from django.shortcuts import get_object_or_404

api = NinjaAPI(urls_namespace='usuarios_api')

@api.get("/usuarios")
def list_users(request):
    return list(Usuario.objects.all().values())

@api.post("/usuarios")
def create_user(request, payload: UsuarioCreateSchema):
    if Usuario.objects.filter(nombre_cuenta=payload.nombre_cuenta).exists():
        raise HttpError(400, f"User with account name {payload.nombre_cuenta} already exists")
    user = Usuario.objects.create(**payload.dict())
    return {
        "id": user.id,
        "nombre": user.nombre,
        "apellido_paterno": user.apellido_paterno,
        "apellido_materno": user.apellido_materno,
        "edad": user.edad,
        "nombre_cuenta": user.nombre_cuenta,
        "contraseña": user.contraseña
    }
@api.get("/usuarios/{user_id}", response=UsuarioSchema)
def get_user(request, user_id: int):
    user = get_object_or_404(Usuario, id=user_id)
    return user

@api.put("/usuarios/{user_id}")
def update_user(request, user_id: int, payload: UsuarioCreateSchema):
    user = get_object_or_404(Usuario, id=user_id)
    for attr, value in payload.dict().items():
        setattr(user, attr, value)
    user.save()
    return {"success": True}

@api.delete("/usuarios/{user_id}")
def delete_user(request, user_id: int):
    user = get_object_or_404(Usuario, id=user_id)
    user.delete()
    return {"success": True}
