# api/app/data/models.py
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.data.db import Base


class Autoparte(Base):
    __tablename__ = "autopartes"

    id          = Column(Integer, primary_key=True, index=True)
    nombre      = Column(String(100), nullable=False)
    categoria   = Column(String(50), nullable=False)
    precio      = Column(Float, nullable=False)
    stock       = Column(Integer, default=0)
    descripcion = Column(Text, nullable=True)

    detalle_pedidos = relationship("DetallePedido", back_populates="autoparte")


class Usuario(Base):
    __tablename__ = "usuarios"

    id       = Column(Integer, primary_key=True, index=True)
    nombre   = Column(String(100), nullable=False)
    email    = Column(String(150), unique=True, nullable=False)
    telefono = Column(String(20), nullable=True)
    password = Column(String(255), nullable=False)
    rol      = Column(String(20), default="cliente")  # cliente | admin

    pedidos = relationship("Pedido", back_populates="usuario")


class Pedido(Base):
    __tablename__ = "pedidos"

    id          = Column(Integer, primary_key=True, index=True)
    usuario_id  = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fecha       = Column(DateTime, default=datetime.utcnow)
    estado      = Column(String(30), default="pendiente")  # pendiente | surtido | enviado | entregado | cancelado
    total       = Column(Float, default=0.0)

    usuario  = relationship("Usuario", back_populates="pedidos")
    detalles = relationship("DetallePedido", back_populates="pedido")


class DetallePedido(Base):
    __tablename__ = "detalle_pedidos"

    id           = Column(Integer, primary_key=True, index=True)
    pedido_id    = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    autoparte_id = Column(Integer, ForeignKey("autopartes.id"), nullable=False)
    cantidad     = Column(Integer, nullable=False)
    precio_unit  = Column(Float, nullable=False)
    subtotal     = Column(Float, nullable=False)

    pedido    = relationship("Pedido", back_populates="detalles")
    autoparte = relationship("Autoparte", back_populates="detalle_pedidos")
