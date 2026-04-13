from flask import render_template, redirect, url_for, flash, request
from app.Services.UsuariosService import UsuariosService

_service = UsuariosService()


def index():
    return render_template("usuarios/index.html", active_view="usuarios", usuarios=_service.all())


def create():
    if request.method == "POST":
        data = {
            "nombre":   request.form["nombre"],
            "email":    request.form["email"],
            "telefono": request.form.get("telefono", ""),
            "password": request.form["password"],
            "rol":      request.form.get("rol", "cliente"),
        }
        _, error = _service.create(data)
        if error:
            flash(f"Error: {error}", "danger")
        else:
            flash("Usuario creado correctamente", "success")
            return redirect(url_for("main.usuarios"))
    return render_template("usuarios/create.html", active_view="usuarios")


def edit(id):
    usuario = _service.find(id)
    if request.method == "POST":
        data = {
            "nombre":   request.form["nombre"],
            "email":    request.form["email"],
            "telefono": request.form.get("telefono", ""),
            "password": request.form.get("password") or None,
            "rol":      request.form.get("rol", "cliente"),
        }
        _, error = _service.update(id, data)
        if error:
            flash(f"Error: {error}", "danger")
        else:
            flash("Usuario actualizado correctamente", "success")
            return redirect(url_for("main.usuarios"))
    return render_template("usuarios/edit.html", active_view="usuarios", usuario=usuario)


def destroy(id):
    _, error = _service.delete(id)
    if error:
        flash(f"Error: {error}", "danger")
    else:
        flash("Usuario eliminado correctamente", "success")
    return redirect(url_for("main.usuarios"))
