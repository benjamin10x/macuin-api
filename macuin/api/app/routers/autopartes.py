from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.data.db import get_db
from app.data.models import Autoparte, DetallePedido
from app.schemas.schemas import AutoparteCreate, AutoparteOut, AutoparteUpdate

router = APIRouter(
    prefix="/v1/autopartes",
    tags=["CRUD Autopartes"],
)

AutoparteId = Annotated[int, Path(..., ge=1, description="ID de la autoparte")]


def _obtener_autoparte_o_404(autoparte_id: int, db: Session) -> Autoparte:
    autoparte = db.query(Autoparte).filter(Autoparte.id == autoparte_id).first()
    if not autoparte:
        raise HTTPException(status_code=404, detail="Autoparte no encontrada")
    return autoparte


@router.get("/", response_model=List[AutoparteOut])
async def listar_autopartes(db: Session = Depends(get_db)):
    return db.query(Autoparte).order_by(Autoparte.id.asc()).all()


@router.get("/{id}", response_model=AutoparteOut)
async def obtener_autoparte(id: AutoparteId, db: Session = Depends(get_db)):
    return _obtener_autoparte_o_404(id, db)


@router.post("/", response_model=AutoparteOut, status_code=status.HTTP_201_CREATED)
async def crear_autoparte(datos: AutoparteCreate, db: Session = Depends(get_db)):
    nueva = Autoparte(**datos.model_dump())
    db.add(nueva)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="No se pudo guardar la autoparte con los datos proporcionados",
        )
    db.refresh(nueva)
    return nueva


@router.put("/{id}", response_model=AutoparteOut)
async def actualizar_autoparte(
    id: AutoparteId,
    datos: AutoparteUpdate,
    db: Session = Depends(get_db),
):
    autoparte = _obtener_autoparte_o_404(id, db)
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(autoparte, campo, valor)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="No se pudo actualizar la autoparte con los datos proporcionados",
        )
    db.refresh(autoparte)
    return autoparte


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_autoparte(id: AutoparteId, db: Session = Depends(get_db)):
    autoparte = _obtener_autoparte_o_404(id, db)
    tiene_detalles = (
        db.query(DetallePedido.id)
        .filter(DetallePedido.autoparte_id == id)
        .first()
    )
    if tiene_detalles:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar la autoparte porque tiene pedidos asociados",
        )

    db.delete(autoparte)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar la autoparte porque tiene relaciones activas",
        )
    return {"mensaje": "Autoparte eliminada correctamente", "id": id}
