from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.data.db import get_db
from app.data.models import Autoparte, DetallePedido, Pedido, Usuario
from app.schemas.schemas import PedidoCreate, PedidoOut, PedidoUpdate

router = APIRouter(
    prefix="/v1/pedidos",
    tags=["Pedidos"],
)

PedidoId = Annotated[int, Path(..., ge=1, description="ID del pedido")]
UsuarioId = Annotated[int, Path(..., ge=1, description="ID del usuario")]


def _obtener_pedido_o_404(pedido_id: int, db: Session) -> Pedido:
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido


def _obtener_usuario_o_404(usuario_id: int, db: Session) -> Usuario:
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.post("/", response_model=PedidoOut, status_code=status.HTTP_201_CREATED)
async def crear_pedido(datos: PedidoCreate, db: Session = Depends(get_db)):
    _obtener_usuario_o_404(datos.usuario_id, db)

    total = 0.0
    detalles_a_guardar = []

    for item in datos.detalles:
        autoparte = db.query(Autoparte).filter(Autoparte.id == item.autoparte_id).first()
        if not autoparte:
            raise HTTPException(
                status_code=404,
                detail=f"Autoparte con id {item.autoparte_id} no encontrada",
            )
        if autoparte.stock < item.cantidad:
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuficiente para '{autoparte.nombre}'. Disponible: {autoparte.stock}",
            )

        subtotal = autoparte.precio * item.cantidad
        total += subtotal
        detalles_a_guardar.append(
            {
                "autoparte": autoparte,
                "cantidad": item.cantidad,
                "precio_unit": autoparte.precio,
                "subtotal": subtotal,
            }
        )

    nuevo_pedido = Pedido(
        usuario_id=datos.usuario_id,
        estado="pendiente",
        total=total,
    )
    db.add(nuevo_pedido)

    try:
        db.flush()
        for detalle_data in detalles_a_guardar:
            detalle = DetallePedido(
                pedido_id=nuevo_pedido.id,
                autoparte_id=detalle_data["autoparte"].id,
                cantidad=detalle_data["cantidad"],
                precio_unit=detalle_data["precio_unit"],
                subtotal=detalle_data["subtotal"],
            )
            db.add(detalle)
            detalle_data["autoparte"].stock -= detalle_data["cantidad"]

        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="No se pudo crear el pedido con los datos proporcionados",
        )

    db.refresh(nuevo_pedido)
    return nuevo_pedido


@router.get("/", response_model=List[PedidoOut])
async def listar_pedidos(db: Session = Depends(get_db)):
    return db.query(Pedido).order_by(Pedido.id.desc()).all()


@router.get("/usuario/{usuario_id}", response_model=List[PedidoOut])
async def pedidos_por_usuario(usuario_id: UsuarioId, db: Session = Depends(get_db)):
    _obtener_usuario_o_404(usuario_id, db)
    return db.query(Pedido).filter(Pedido.usuario_id == usuario_id).order_by(Pedido.id.desc()).all()


@router.get("/{id}", response_model=PedidoOut)
async def obtener_pedido(id: PedidoId, db: Session = Depends(get_db)):
    return _obtener_pedido_o_404(id, db)


@router.put("/{id}", response_model=PedidoOut)
async def actualizar_pedido(
    id: PedidoId,
    datos: PedidoUpdate,
    db: Session = Depends(get_db),
):
    pedido = _obtener_pedido_o_404(id, db)
    pedido.estado = datos.estado

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="No se pudo actualizar el pedido con los datos proporcionados",
        )
    db.refresh(pedido)
    return pedido
