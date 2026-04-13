import os
import requests
from flask import render_template, redirect, url_for, flash, Response

API_URL = os.getenv("API_URL", "http://api:8000/v1")

_TIPOS_VALIDOS = {"inventario", "bajo-stock", "ventas", "top-productos"}
_FMTS_VALIDOS  = {"pdf", "xlsx", "docx"}


def index():
    return render_template("reportes/index.html", active_view="reportes")


def download(tipo, fmt):
    if tipo not in _TIPOS_VALIDOS or fmt not in _FMTS_VALIDOS:
        flash("Reporte no válido", "danger")
        return redirect(url_for("main.reportes"))
    try:
        r = requests.get(f"{API_URL}/reportes/{tipo}/{fmt}", timeout=15, stream=True)
        r.raise_for_status()
        return Response(
            r.content,
            content_type=r.headers.get("Content-Type", "application/octet-stream"),
            headers={"Content-Disposition": r.headers.get("Content-Disposition", f"attachment; filename={tipo}.{fmt}")},
        )
    except Exception as e:
        flash(f"Error generando reporte: {e}", "danger")
        return redirect(url_for("main.reportes"))
