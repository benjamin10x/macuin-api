# api/app/routers/pedidos.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.data.db import get_db
from app.data.models import Pedido, DetallePedido, Autoparte, Usuario
from app.schemas.schemas import PedidoCreate, PedidoOut

router = APIRouter(
    prefix="/v1/pedidos",
    tags=["Pedidos"]
)


@router.post("/", response_model=PedidoOut, status_code=status.HTTP_201_CREATED)
async def crear_pedido(datos: PedidoCreate, db: Session = Depends(get_db)):
    """
    Crear pedido con 1 a N productos.
    Valida stock antes de confirmar y lo descuenta al crear.
    """
    # Verificar que el usuario existe
    usuario = db.query(Usuario).filter(Usuario.id == datos.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    total = 0.0
    detalles_a_guardar = []

    for item in datos.detalles:
        autoparte = db.query(Autoparte).filter(Autoparte.id == item.autoparte_id).first()
        if not autoparte:
            raise HTTPException(
                status_code=404,
                detail=f"Autoparte con id {item.autoparte_id} no encontrada"
            )
        if autoparte.stock < item.cantidad:
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuficiente para '{autoparte.nombre}'. Disponible: {autoparte.stock}"
            )
        subtotal = autoparte.precio * item.cantidad
        total += subtotal
        detalles_a_guardar.append({
            "autoparte": autoparte,
            "cantidad": item.cantidad,
            "precio_unit": autoparte.precio,
            "subtotal": subtotal
        })

    # Crear pedido
    nuevo_pedido = Pedido(
        usuario_id=datos.usuario_id,
        estado="pendiente",
        total=total
    )
    db.add(nuevo_pedido)
    db.flush()  # Obtener ID sin hacer commit aún

    # Crear detalles y descontar stock
    for d in detalles_a_guardar:
        detalle = DetallePedido(
            pedido_id=nuevo_pedido.id,
            autoparte_id=d["autoparte"].id,
            cantidad=d["cantidad"],
            precio_unit=d["precio_unit"],
            subtotal=d["subtotal"]
        )
        db.add(detalle)
        d["autoparte"].stock -= d["cantidad"]

    db.commit()
    db.refresh(nuevo_pedido)
    return nuevo_pedido


@router.get("/", response_model=List[PedidoOut])
async def listar_pedidos(db: Session = Depends(get_db)):
    """Listar todos los pedidos (admin Flask)."""
    return db.query(Pedido).all()


@router.get("/usuario/{usuario_id}", response_model=List[PedidoOut])
async def pedidos_por_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Todos los pedidos de un usuario (Laravel)."""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db.query(Pedido).filter(Pedido.usuario_id == usuario_id).all()


@router.get("/{id}", response_model=PedidoOut)
async def obtener_pedido(id: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido
