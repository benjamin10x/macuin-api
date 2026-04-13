# api/app/routers/usuarios.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import hashlib

from app.data.db import get_db
from app.data.models import Usuario
from app.schemas.schemas import UsuarioCreate, UsuarioUpdate, UsuarioOut

router = APIRouter(
    prefix="/v1/usuarios",
    tags=["CRUD Usuarios"]
)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# ── Registro externo (clientes desde Laravel) ──────────────────
@router.post("/registro", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
async def registrar_usuario_externo(datos: UsuarioCreate, db: Session = Depends(get_db)):
    """Endpoint para que clientes se registren desde Laravel."""
    existente = db.query(Usuario).filter(Usuario.email == datos.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    nuevo = Usuario(
        nombre=datos.nombre,
        email=datos.email,
        telefono=datos.telefono,
        password=hash_password(datos.password),
        rol="cliente"
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


# ── CRUD interno (admin desde Flask) ───────────────────────────
@router.get("/", response_model=List[UsuarioOut])
async def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()


@router.get("/{id}", response_model=UsuarioOut)
async def obtener_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.post("/", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
async def crear_usuario_interno(datos: UsuarioCreate, db: Session = Depends(get_db)):
    """Crear usuario interno (admin) desde Flask."""
    existente = db.query(Usuario).filter(Usuario.email == datos.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    nuevo = Usuario(
        nombre=datos.nombre,
        email=datos.email,
        telefono=datos.telefono,
        password=hash_password(datos.password),
        rol=datos.rol or "cliente"
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.put("/{id}", response_model=UsuarioOut)
async def actualizar_usuario(id: int, datos: UsuarioUpdate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.nombre   = datos.nombre
    usuario.email    = datos.email
    usuario.telefono = datos.telefono
    usuario.rol      = datos.rol or usuario.rol
    if datos.password:
        usuario.password = hash_password(datos.password)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return {"mensaje": "Usuario eliminado correctamente", "id": id}
