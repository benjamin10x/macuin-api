from flask import render_template, redirect, url_for, flash, request
from app.Services.AutopartesService import AutopartesService

_service = AutopartesService()


def index():
    return render_template("autopartes/index.html", active_view="autopartes", autopartes=_service.all())


def create():
    if request.method == "POST":
        data = {
            "nombre":      request.form["nombre"],
            "categoria":   request.form["categoria"],
            "precio":      float(request.form["precio"]),
            "stock":       int(request.form["stock"]),
            "descripcion": request.form.get("descripcion", ""),
        }
        _, error = _service.create(data)
        if error:
            flash(f"Error: {error}", "danger")
        else:
            flash("Autoparte creada correctamente", "success")
            return redirect(url_for("main.autopartes"))
    return render_template("autopartes/create.html", active_view="autopartes")


def edit(id):
    autoparte = _service.find(id)
    if request.method == "POST":
        data = {
            "nombre":      request.form["nombre"],
            "categoria":   request.form["categoria"],
            "precio":      float(request.form["precio"]),
            "stock":       int(request.form["stock"]),
            "descripcion": request.form.get("descripcion", ""),
        }
        _, error = _service.update(id, data)
        if error:
            flash(f"Error: {error}", "danger")
        else:
            flash("Autoparte actualizada correctamente", "success")
            return redirect(url_for("main.autopartes"))
    return render_template("autopartes/edit.html", active_view="autopartes", autoparte=autoparte)


def destroy(id):
    _, error = _service.delete(id)
    if error:
        flash(f"Error: {error}", "danger")
    else:
        flash("Autoparte eliminada correctamente", "success")
    return redirect(url_for("main.autopartes"))
