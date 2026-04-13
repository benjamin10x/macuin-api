from app.Services.BaseService import BaseService


class UsuariosService(BaseService):
    def all(self):
        return self._get("/usuarios/")

    def find(self, id):
        return self._get(f"/usuarios/{id}")

    def create(self, data):
        return self._post("/usuarios/", data)

    def update(self, id, data):
        return self._put(f"/usuarios/{id}", data)

    def delete(self, id):
        return self._delete(f"/usuarios/{id}")
