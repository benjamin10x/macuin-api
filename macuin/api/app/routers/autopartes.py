# api/app/routers/autopartes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.data.db import get_db
from app.data.models import Autoparte
from app.schemas.schemas import AutoparteCreate, AutoparteUpdate, AutoparteOut

router = APIRouter(
    prefix="/v1/autopartes",
    tags=["CRUD Autopartes"]
)


@router.get("/", response_model=List[AutoparteOut])
async def listar_autopartes(db: Session = Depends(get_db)):
    autopartes = db.query(Autoparte).all()
    return autopartes


@router.get("/{id}", response_model=AutoparteOut)
async def obtener_autoparte(id: int, db: Session = Depends(get_db)):
    autoparte = db.query(Autoparte).filter(Autoparte.id == id).first()
    if not autoparte:
        raise HTTPException(status_code=404, detail="Autoparte no encontrada")
    return autoparte


@router.post("/", response_model=AutoparteOut, status_code=status.HTTP_201_CREATED)
async def crear_autoparte(datos: AutoparteCreate, db: Session = Depends(get_db)):
    nueva = Autoparte(
        nombre=datos.nombre,
        categoria=datos.categoria,
        precio=datos.precio,
        stock=datos.stock,
        descripcion=datos.descripcion
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


@router.put("/{id}", response_model=AutoparteOut)
async def actualizar_autoparte(id: int, datos: AutoparteUpdate, db: Session = Depends(get_db)):
    autoparte = db.query(Autoparte).filter(Autoparte.id == id).first()
    if not autoparte:
        raise HTTPException(status_code=404, detail="Autoparte no encontrada")
    autoparte.nombre      = datos.nombre
    autoparte.categoria   = datos.categoria
    autoparte.precio      = datos.precio
    autoparte.stock       = datos.stock
    autoparte.descripcion = datos.descripcion
    db.commit()
    db.refresh(autoparte)
    return autoparte


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_autoparte(id: int, db: Session = Depends(get_db)):
    autoparte = db.query(Autoparte).filter(Autoparte.id == id).first()
    if not autoparte:
        raise HTTPException(status_code=404, detail="Autoparte no encontrada")
    db.delete(autoparte)
    db.commit()
    return {"mensaje": "Autoparte eliminada correctamente", "id": id}
