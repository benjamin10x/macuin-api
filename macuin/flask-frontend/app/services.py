# flask-frontend/app/services.py
import requests
import os

API_URL = os.getenv("API_URL", "http://api:8000/v1")


def _get(endpoint):
    try:
        r = requests.get(f"{API_URL}{endpoint}", timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[API ERROR GET] {endpoint}: {e}")
        return []


def _post(endpoint, data):
    try:
        r = requests.post(f"{API_URL}{endpoint}", json=data, timeout=5)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.HTTPError as e:
        try:
            detalle = e.response.json().get("detail", str(e))
        except Exception:
            detalle = str(e)
        return None, detalle
    except Exception as e:
        return None, str(e)


def _put(endpoint, data):
    try:
        r = requests.put(f"{API_URL}{endpoint}", json=data, timeout=5)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.HTTPError as e:
        try:
            detalle = e.response.json().get("detail", str(e))
        except Exception:
            detalle = str(e)
        return None, detalle
    except Exception as e:
        return None, str(e)


def _delete(endpoint):
    try:
        r = requests.delete(f"{API_URL}{endpoint}", timeout=5)
        r.raise_for_status()
        return True, None
    except Exception as e:
        return False, str(e)


# ── Autopartes ─────────────────────────────────────────────────
def get_all_autopartes():
    return _get("/autopartes/")

def get_autoparte(id):
    return _get(f"/autopartes/{id}")

def create_autoparte(data):
    return _post("/autopartes/", data)

def update_autoparte(id, data):
    return _put(f"/autopartes/{id}", data)

def delete_autoparte(id):
    return _delete(f"/autopartes/{id}")


# ── Usuarios ───────────────────────────────────────────────────
def get_all_usuarios():
    return _get("/usuarios/")

def get_usuario(id):
    return _get(f"/usuarios/{id}")

def create_usuario(data):
    return _post("/usuarios/", data)

def update_usuario(id, data):
    return _put(f"/usuarios/{id}", data)

def delete_usuario(id):
    return _delete(f"/usuarios/{id}")


# ── Pedidos ────────────────────────────────────────────────────
def get_all_pedidos():
    return _get("/pedidos/")
