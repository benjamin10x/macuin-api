from datetime import datetime
from enum import Enum
from typing import Any, List, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    ValidationInfo,
    field_validator,
    model_validator,
)


def _strip_text(value: Any) -> Any:
    if isinstance(value, str):
        return value.strip()
    return value


def _strip_lower_text(value: Any) -> Any:
    if isinstance(value, str):
        return value.strip().lower()
    return value


def _blank_to_none(value: Any) -> Any:
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return value


def _reject_bool(value: Any) -> Any:
    if isinstance(value, bool):
        raise ValueError("No se permiten valores booleanos en este campo")
    return value


class APIBaseModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        use_enum_values=True,
    )


class RolUsuario(str, Enum):
    cliente = "cliente"
    admin = "admin"


class EstadoPedido(str, Enum):
    pendiente = "pendiente"
    surtido = "surtido"
    enviado = "enviado"
    entregado = "entregado"
    cancelado = "cancelado"


class AutoparteBase(APIBaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, examples=["Filtro de Aceite"])
    categoria: str = Field(..., min_length=2, max_length=50, examples=["Filtros"])
    precio: float = Field(..., gt=0, examples=[15.99])
    stock: int = Field(..., ge=0, examples=[45])
    descripcion: Optional[str] = Field(
        default=None,
        max_length=500,
        examples=["Filtro de aceite para motor 4 cilindros"],
    )

    @field_validator("nombre", "categoria", mode="before")
    @classmethod
    def limpiar_texto_requerido(cls, value: Any) -> Any:
        return _strip_text(value)

    @field_validator("descripcion", mode="before")
    @classmethod
    def limpiar_descripcion(cls, value: Any) -> Any:
        return _blank_to_none(value)

    @field_validator("precio", "stock", mode="before")
    @classmethod
    def validar_campos_numericos(cls, value: Any) -> Any:
        return _reject_bool(value)


class AutoparteCreate(AutoparteBase):
    pass


class AutoparteUpdate(APIBaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=100, examples=["Filtro de Aceite"])
    categoria: Optional[str] = Field(None, min_length=2, max_length=50, examples=["Filtros"])
    precio: Optional[float] = Field(None, gt=0, examples=[15.99])
    stock: Optional[int] = Field(None, ge=0, examples=[45])
    descripcion: Optional[str] = Field(
        default=None,
        max_length=500,
        examples=["Filtro de aceite para motor 4 cilindros"],
    )

    @field_validator("nombre", "categoria", mode="before")
    @classmethod
    def limpiar_texto_opcional(cls, value: Any) -> Any:
        return _strip_text(value)

    @field_validator("descripcion", mode="before")
    @classmethod
    def limpiar_descripcion(cls, value: Any) -> Any:
        return _blank_to_none(value)

    @field_validator("nombre", "categoria", "precio", "stock", mode="before")
    @classmethod
    def prohibir_nulos(cls, value: Any, info: ValidationInfo) -> Any:
        if value is None:
            raise ValueError(f"El campo '{info.field_name}' no puede ser nulo")
        return value

    @field_validator("precio", "stock", mode="before")
    @classmethod
    def validar_campos_numericos(cls, value: Any) -> Any:
        return _reject_bool(value)

    @model_validator(mode="after")
    def validar_payload_no_vacio(self):
        if not self.model_fields_set:
            raise ValueError("Debes enviar al menos un campo para actualizar la autoparte")
        return self


class AutoparteOut(AutoparteBase):
    id: int = Field(..., ge=1, examples=[1])


class UsuarioBase(APIBaseModel):
    nombre: str = Field(..., min_length=3, max_length=100, examples=["Juan Perez"])
    email: EmailStr = Field(..., examples=["juan@correo.com"])
    telefono: Optional[str] = Field(
        default=None,
        min_length=10,
        max_length=15,
        pattern=r"^\+?\d{10,15}$",
        examples=["5551234567"],
    )

    @field_validator("nombre", mode="before")
    @classmethod
    def limpiar_nombre(cls, value: Any) -> Any:
        return _strip_text(value)

    @field_validator("email", mode="before")
    @classmethod
    def limpiar_email(cls, value: Any) -> Any:
        return _strip_lower_text(value)

    @field_validator("telefono", mode="before")
    @classmethod
    def limpiar_telefono(cls, value: Any) -> Any:
        return _blank_to_none(value)


class UsuarioRegistro(UsuarioBase):
    password: str = Field(..., min_length=6, max_length=128, examples=["segura123"])

    @field_validator("password")
    @classmethod
    def validar_password(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("La contraseña no puede estar vacia")
        return value


class UsuarioCreate(UsuarioRegistro):
    rol: RolUsuario = Field(default=RolUsuario.cliente, examples=["cliente"])

    @field_validator("rol", mode="before")
    @classmethod
    def limpiar_rol(cls, value: Any) -> Any:
        return _strip_lower_text(value)


class UsuarioLogin(APIBaseModel):
    email: EmailStr = Field(..., examples=["juan@correo.com"])
    password: str = Field(..., min_length=6, max_length=128, examples=["segura123"])

    @field_validator("email", mode="before")
    @classmethod
    def limpiar_email(cls, value: Any) -> Any:
        return _strip_lower_text(value)

    @field_validator("password")
    @classmethod
    def validar_password(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("La contraseña no puede estar vacia")
        return value


class UsuarioUpdate(APIBaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=100, examples=["Juan Perez"])
    email: Optional[EmailStr] = Field(None, examples=["juan@correo.com"])
    telefono: Optional[str] = Field(
        default=None,
        min_length=10,
        max_length=15,
        pattern=r"^\+?\d{10,15}$",
        examples=["5551234567"],
    )
    rol: Optional[RolUsuario] = Field(None, examples=["cliente"])
    password: Optional[str] = Field(None, min_length=6, max_length=128, examples=["segura123"])

    @field_validator("nombre", mode="before")
    @classmethod
    def limpiar_nombre(cls, value: Any) -> Any:
        return _strip_text(value)

    @field_validator("email", "rol", mode="before")
    @classmethod
    def limpiar_campos_minusculas(cls, value: Any) -> Any:
        return _strip_lower_text(value)

    @field_validator("telefono", mode="before")
    @classmethod
    def limpiar_telefono(cls, value: Any) -> Any:
        return _blank_to_none(value)

    @field_validator("nombre", "email", "rol", "password", mode="before")
    @classmethod
    def prohibir_nulos(cls, value: Any, info: ValidationInfo) -> Any:
        if value is None:
            raise ValueError(f"El campo '{info.field_name}' no puede ser nulo")
        return value

    @field_validator("password")
    @classmethod
    def validar_password(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value.strip():
            raise ValueError("La contraseña no puede estar vacia")
        return value

    @model_validator(mode="after")
    def validar_payload_no_vacio(self):
        if not self.model_fields_set:
            raise ValueError("Debes enviar al menos un campo para actualizar el usuario")
        return self


class UsuarioOut(UsuarioBase):
    id: int = Field(..., ge=1, examples=[1])
    rol: RolUsuario = Field(..., examples=["cliente"])


class DetalleIn(APIBaseModel):
    autoparte_id: int = Field(..., ge=1, examples=[1])
    cantidad: int = Field(..., ge=1, le=999, examples=[2])

    @field_validator("autoparte_id", "cantidad", mode="before")
    @classmethod
    def validar_campos_numericos(cls, value: Any) -> Any:
        return _reject_bool(value)


class PedidoCreate(APIBaseModel):
    usuario_id: int = Field(..., ge=1, examples=[1])
    detalles: List[DetalleIn] = Field(..., min_length=1, max_length=100)

    @field_validator("usuario_id", mode="before")
    @classmethod
    def validar_usuario_id(cls, value: Any) -> Any:
        return _reject_bool(value)

    @model_validator(mode="after")
    def validar_autopartes_repetidas(self):
        ids = [detalle.autoparte_id for detalle in self.detalles]
        repetidos = sorted({autoparte_id for autoparte_id in ids if ids.count(autoparte_id) > 1})
        if repetidos:
            raise ValueError(
                f"No se permiten autopartes repetidas en el mismo pedido: {', '.join(map(str, repetidos))}"
            )
        return self


class PedidoUpdate(APIBaseModel):
    estado: EstadoPedido = Field(..., examples=["enviado"])

    @field_validator("estado", mode="before")
    @classmethod
    def limpiar_estado(cls, value: Any) -> Any:
        return _strip_lower_text(value)


class DetalleOut(APIBaseModel):
    autoparte_id: int = Field(..., ge=1)
    cantidad: int = Field(..., ge=1)
    precio_unit: float = Field(..., ge=0)
    subtotal: float = Field(..., ge=0)
    autoparte: Optional[AutoparteOut] = None


class PedidoOut(APIBaseModel):
    id: int = Field(..., ge=1)
    usuario_id: int = Field(..., ge=1)
    fecha: datetime
    estado: EstadoPedido
    total: float = Field(..., ge=0)
    detalles: List[DetalleOut] = Field(default_factory=list)
