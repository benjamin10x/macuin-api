# api/app/schemas/schemas.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime


# ─── AUTOPARTE ─────────────────────────────────────────────────
class AutoparteBase(BaseModel):
    nombre:      str   = Field(..., min_length=2, max_length=100, example="Filtro de Aceite")
    categoria:   str   = Field(..., min_length=2, max_length=50,  example="Filtros")
    precio:      float = Field(..., gt=0,                          example=15.99)
    stock:       int   = Field(..., ge=0,                          example=45)
    descripcion: Optional[str] = Field(None,                       example="Filtro de aceite para motor 4 cilindros")

class AutoparteCreate(AutoparteBase):
    pass

class AutoparteUpdate(AutoparteBase):
    pass

class AutoparteOut(AutoparteBase):
    id: int
    class Config:
        from_attributes = True


# ─── USUARIO ────────────────────────────────────────────────────
class UsuarioBase(BaseModel):
    nombre:   str = Field(..., min_length=3, max_length=100, example="Juan Pérez")
    email:    str = Field(...,                               example="juan@correo.com")
    telefono: Optional[str] = Field(None,                   example="5551234567")
    rol:      Optional[str] = Field("cliente",               example="cliente")

class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=6, example="segura123")

class UsuarioUpdate(UsuarioBase):
    password: Optional[str] = None

class UsuarioOut(UsuarioBase):
    id: int
    class Config:
        from_attributes = True


# ─── PEDIDO ─────────────────────────────────────────────────────
class DetalleIn(BaseModel):
    autoparte_id: int = Field(..., example=1)
    cantidad:     int = Field(..., ge=1, le=999, example=2)

class PedidoCreate(BaseModel):
    usuario_id: int           = Field(..., example=1)
    detalles:   List[DetalleIn] = Field(..., min_length=1)

class PedidoUpdate(BaseModel):
    estado: str = Field(..., example="enviado")

class DetalleOut(BaseModel):
    autoparte_id: int
    cantidad:     int
    precio_unit:  float
    subtotal:     float
    autoparte:    Optional[AutoparteOut] = None
    class Config:
        from_attributes = True

class PedidoOut(BaseModel):
    id:         int
    usuario_id: int
    fecha:      datetime
    estado:     str
    total:      float
    detalles:   List[DetalleOut] = []
    class Config:
        from_attributes = True
