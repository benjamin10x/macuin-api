from flask import render_template
from app.Services.PedidosService import PedidosService

_service = PedidosService()


def index():
    return render_template("pedidos/index.html", active_view="pedidos", pedidos=_service.all())
