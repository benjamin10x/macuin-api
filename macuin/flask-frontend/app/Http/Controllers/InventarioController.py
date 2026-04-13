from flask import render_template
from app.Services.AutopartesService import AutopartesService

_service = AutopartesService()


def index():
    autopartes  = _service.all()
    total_valor = sum(a["precio"] * a["stock"] for a in autopartes) if autopartes else 0
    bajo_stock  = [a for a in autopartes if a["stock"] < 10] if autopartes else []
    return render_template(
        "inventario/index.html",
        active_view="inventario",
        autopartes=autopartes,
        total_valor=total_valor,
        bajo_stock=bajo_stock,
    )
