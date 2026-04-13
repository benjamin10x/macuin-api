from flask import Blueprint
from app.Http.Controllers import (
    DashboardController,
    AutopartesController,
    UsuariosController,
    PedidosController,
    InventarioController,
    ReportesController,
)

web = Blueprint("main", __name__)

# ── Dashboard ──────────────────────────────────────────────────
web.add_url_rule("/", view_func=DashboardController.index)

# ── Autopartes ─────────────────────────────────────────────────
web.add_url_rule("/autopartes",                    view_func=AutopartesController.index)
web.add_url_rule("/autopartes/nuevo",              view_func=AutopartesController.create,  methods=["GET", "POST"])
web.add_url_rule("/autopartes/<int:id>/editar",    view_func=AutopartesController.edit,    methods=["GET", "POST"])
web.add_url_rule("/autopartes/<int:id>/eliminar",  view_func=AutopartesController.destroy, methods=["POST"])

# ── Usuarios ───────────────────────────────────────────────────
web.add_url_rule("/usuarios",                   view_func=UsuariosController.index)
web.add_url_rule("/usuarios/nuevo",             view_func=UsuariosController.create,  methods=["GET", "POST"])
web.add_url_rule("/usuarios/<int:id>/editar",   view_func=UsuariosController.edit,    methods=["GET", "POST"])
web.add_url_rule("/usuarios/<int:id>/eliminar", view_func=UsuariosController.destroy, methods=["POST"])

# ── Pedidos ────────────────────────────────────────────────────
web.add_url_rule("/pedidos", view_func=PedidosController.index)

# ── Inventario ─────────────────────────────────────────────────
web.add_url_rule("/inventario", view_func=InventarioController.index)

# ── Reportes ───────────────────────────────────────────────────
web.add_url_rule("/reportes",              view_func=ReportesController.index)
web.add_url_rule("/reportes/<tipo>/<fmt>", view_func=ReportesController.download)
