from typing import Annotated, List, Optional
import hashlib

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.data.db import get_db
from app.data.models import Pedido, Usuario
from app.schemas.schemas import (
    UsuarioCreate,
    UsuarioLogin,
    UsuarioOut,
    UsuarioRegistro,
    UsuarioUpdate,
)

router = APIRouter(
    prefix="/v1/usuarios",
    tags=["CRUD Usuarios"],
)

UsuarioId = Annotated[int, Path(..., ge=1, description="ID del usuario")]


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def _obtener_usuario_o_404(usuario_id: int, db: Session) -> Usuario:
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


def _buscar_email_existente(
    email: str,
    db: Session,
    usuario_id_excluido: Optional[int] = None,
) -> Optional[Usuario]:
    query = db.query(Usuario).filter(Usuario.email == email)
    if usuario_id_excluido is not None:
        query = query.filter(Usuario.id != usuario_id_excluido)
    return query.first()


@router.post("/registro", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
async def registrar_usuario_externo(datos: UsuarioRegistro, db: Session = Depends(get_db)):
    existente = _buscar_email_existente(datos.email, db)
    if existente:
        raise HTTPException(status_code=409, detail="El email ya esta registrado")

    nuevo = Usuario(
        nombre=datos.nombre,
        email=datos.email,
        telefono=datos.telefono,
        password=hash_password(datos.password),
        rol="cliente",
    )
    db.add(nuevo)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="El email ya esta registrado")
    db.refresh(nuevo)
    return nuevo


@router.post("/login", response_model=UsuarioOut, status_code=status.HTTP_200_OK)
async def iniciar_sesion(datos: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == datos.email).first()
    if not usuario or usuario.password != hash_password(datos.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
        )
    return usuario


@router.get("/", response_model=List[UsuarioOut])
async def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).order_by(Usuario.id.asc()).all()


@router.get("/{id}", response_model=UsuarioOut)
async def obtener_usuario(id: UsuarioId, db: Session = Depends(get_db)):
    return _obtener_usuario_o_404(id, db)


@router.post("/", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
async def crear_usuario_interno(datos: UsuarioCreate, db: Session = Depends(get_db)):
    existente = _buscar_email_existente(datos.email, db)
    if existente:
        raise HTTPException(status_code=409, detail="El email ya esta registrado")

    nuevo = Usuario(
        nombre=datos.nombre,
        email=datos.email,
        telefono=datos.telefono,
        password=hash_password(datos.password),
        rol=datos.rol,
    )
    db.add(nuevo)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="El email ya esta registrado")
    db.refresh(nuevo)
    return nuevo


@router.put("/{id}", response_model=UsuarioOut)
async def actualizar_usuario(
    id: UsuarioId,
    datos: UsuarioUpdate,
    db: Session = Depends(get_db),
):
    usuario = _obtener_usuario_o_404(id, db)
    cambios = datos.model_dump(exclude_unset=True)

    email = cambios.get("email")
    if email and _buscar_email_existente(email, db, usuario_id_excluido=id):
        raise HTTPException(status_code=409, detail="El email ya esta registrado")

    password = cambios.pop("password", None)
    for campo, valor in cambios.items():
        setattr(usuario, campo, valor)

    if password is not None:
        usuario.password = hash_password(password)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="No se pudo actualizar el usuario con los datos proporcionados",
        )
    db.refresh(usuario)
    return usuario


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: UsuarioId, db: Session = Depends(get_db)):
    usuario = _obtener_usuario_o_404(id, db)
    tiene_pedidos = db.query(Pedido.id).filter(Pedido.usuario_id == id).first()
    if tiene_pedidos:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar el usuario porque tiene pedidos asociados",
        )

    db.delete(usuario)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar el usuario porque tiene relaciones activas",
        )
    return {"mensaje": "Usuario eliminado correctamente", "id": id}
