from flask import render_template
from app.Services.AutopartesService import AutopartesService
from app.Services.UsuariosService import UsuariosService
from app.Services.PedidosService import PedidosService

_autopartes = AutopartesService()
_usuarios   = UsuariosService()
_pedidos    = PedidosService()


def index():
    autopartes  = _autopartes.all()
    usuarios    = _usuarios.all()
    pedidos     = _pedidos.all()
    total_valor = sum(a["precio"] * a["stock"] for a in autopartes) if autopartes else 0
    bajo_stock  = [a for a in autopartes if a["stock"] < 10] if autopartes else []
    return render_template(
        "dashboard/index.html",
        active_view="dashboard",
        autopartes=autopartes,
        usuarios=usuarios,
        pedidos=pedidos,
        total_valor=total_valor,
        bajo_stock=bajo_stock,
    )
