# flask-frontend/app/routes.py
import os
import requests
from flask import Blueprint, render_template, redirect, url_for, flash, request, Response

main = Blueprint("main", __name__)

API_URL = os.getenv("API_URL", "http://api:8000/v1")

from app.services import (
    get_all_autopartes, get_autoparte, create_autoparte,
    update_autoparte, delete_autoparte,
    get_all_usuarios, get_usuario, create_usuario,
    update_usuario, delete_usuario,
    get_all_pedidos
)


# ══════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════
@main.route("/")
def index():
    autopartes = get_all_autopartes()
    usuarios   = get_all_usuarios()
    pedidos    = get_all_pedidos()
    total_valor = sum(a["precio"] * a["stock"] for a in autopartes) if autopartes else 0
    bajo_stock  = [a for a in autopartes if a["stock"] < 10] if autopartes else []
    return render_template("index.html",
        autopartes=autopartes, usuarios=usuarios, pedidos=pedidos,
        total_valor=total_valor, bajo_stock=bajo_stock)


# ══════════════════════════════════════════════════════════════
# AUTOPARTES
# ══════════════════════════════════════════════════════════════
@main.route("/autopartes")
def autopartes():
    data = get_all_autopartes()
    return render_template("autopartes.html", autopartes=data)


@main.route("/autopartes/nuevo", methods=["GET", "POST"])
def nuevo_autoparte():
    if request.method == "POST":
        data = {
            "nombre":      request.form["nombre"],
            "categoria":   request.form["categoria"],
            "precio":      float(request.form["precio"]),
            "stock":       int(request.form["stock"]),
            "descripcion": request.form.get("descripcion", "")
        }
        resultado, error = create_autoparte(data)
        if error:
            flash(f"Error: {error}", "danger")
        else:
            flash("Autoparte creada correctamente", "success")
            return redirect(url_for("main.autopartes"))
    return render_template("nuevo_autoparte.html")


@main.route("/autopartes/<int:id>/editar", methods=["GET", "POST"])
def editar_autoparte(id):
    autoparte = get_autoparte(id)
    if request.method == "POST":
        data = {
            "nombre":      request.form["nombre"],
            "categoria":   request.form["categoria"],
            "precio":      float(request.form["precio"]),
            "stock":       int(request.form["stock"]),
            "descripcion": request.form.get("descripcion", "")
        }
        resultado, error = update_autoparte(id, data)
        if error:
            flash(f"Error: {error}", "danger")
        else:
            flash("Autoparte actualizada correctamente", "success")
            return redirect(url_for("main.autopartes"))
    return render_template("editar_autoparte.html", autoparte=autoparte)


@main.route("/autopartes/<int:id>/eliminar", methods=["POST"])
def eliminar_autoparte(id):
    ok, error = delete_autoparte(id)
    if error:
        flash(f"Error: {error}", "danger")
    else:
        flash("Autoparte eliminada correctamente", "success")
    return redirect(url_for("main.autopartes"))


# ══════════════════════════════════════════════════════════════
# USUARIOS
# ══════════════════════════════════════════════════════════════
@main.route("/usuarios")
def usuarios():
    data = get_all_usuarios()
    return render_template("usuarios.html", usuarios=data)


@main.route("/usuarios/nuevo", methods=["GET", "POST"])
def nuevo_usuario():
    if request.method == "POST":
        data = {
            "nombre":   request.form["nombre"],
            "email":    request.form["email"],
            "telefono": request.form.get("telefono", ""),
            "password": request.form["password"],
            "rol":      request.form.get("rol", "cliente")
        }
        resultado, error = create_usuario(data)
        if error:
            flash(f"Error: {error}", "danger")
        else:
            flash("Usuario creado correctamente", "success")
            return redirect(url_for("main.usuarios"))
    return render_template("nuevo_usuario.html")


@main.route("/usuarios/<int:id>/editar", methods=["GET", "POST"])
def editar_usuario(id):
    usuario = get_usuario(id)
    if request.method == "POST":
        data = {
            "nombre":   request.form["nombre"],
            "email":    request.form["email"],
            "telefono": request.form.get("telefono", ""),
            "password": request.form.get("password") or None,
            "rol":      request.form.get("rol", "cliente")
        }
        resultado, error = update_usuario(id, data)
        if error:
            flash(f"Error: {error}", "danger")
        else:
            flash("Usuario actualizado correctamente", "success")
            return redirect(url_for("main.usuarios"))
    return render_template("editar_usuario.html", usuario=usuario)


@main.route("/usuarios/<int:id>/eliminar", methods=["POST"])
def eliminar_usuario(id):
    ok, error = delete_usuario(id)
    if error:
        flash(f"Error: {error}", "danger")
    else:
        flash("Usuario eliminado correctamente", "success")
    return redirect(url_for("main.usuarios"))


# ══════════════════════════════════════════════════════════════
# PEDIDOS
# ══════════════════════════════════════════════════════════════
@main.route("/pedidos")
def pedidos():
    data = get_all_pedidos()
    return render_template("pedidos.html", pedidos=data)


# ══════════════════════════════════════════════════════════════
# INVENTARIO
# ══════════════════════════════════════════════════════════════
@main.route("/inventario")
def inventario():
    autopartes  = get_all_autopartes()
    total_valor = sum(a["precio"] * a["stock"] for a in autopartes) if autopartes else 0
    bajo_stock  = [a for a in autopartes if a["stock"] < 10] if autopartes else []
    return render_template("inventario.html",
        autopartes=autopartes, total_valor=total_valor, bajo_stock=bajo_stock)


# ══════════════════════════════════════════════════════════════
# REPORTES — proxy de descarga desde la API
# ══════════════════════════════════════════════════════════════
@main.route("/reportes")
def reportes():
    return render_template("reportes.html")


@main.route("/reportes/<tipo>/<fmt>")
def descargar_reporte(tipo, fmt):
    """Proxy: Flask descarga el archivo de la API y lo envía al navegador."""
    tipos_validos = ["inventario", "bajo-stock", "ventas", "top-productos"]
    fmts_validos  = ["pdf", "xlsx", "docx"]
    if tipo not in tipos_validos or fmt not in fmts_validos:
        flash("Reporte no válido", "danger")
        return redirect(url_for("main.reportes"))

    try:
        r = requests.get(f"{API_URL}/reportes/{tipo}/{fmt}", timeout=15, stream=True)
        r.raise_for_status()
        content_type = r.headers.get("Content-Type", "application/octet-stream")
        disposition  = r.headers.get("Content-Disposition", f"attachment; filename={tipo}.{fmt}")
        return Response(r.content, content_type=content_type,
                        headers={"Content-Disposition": disposition})
    except Exception as e:
        flash(f"Error generando reporte: {e}", "danger")
        return redirect(url_for("main.reportes"))
