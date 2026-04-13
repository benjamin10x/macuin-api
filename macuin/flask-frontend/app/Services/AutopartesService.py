from app.Services.BaseService import BaseService


class AutopartesService(BaseService):
    def all(self):
        return self._get("/autopartes/")

    def find(self, id):
        return self._get(f"/autopartes/{id}")

    def create(self, data):
        return self._post("/autopartes/", data)

    def update(self, id, data):
        return self._put(f"/autopartes/{id}", data)

    def delete(self, id):
        return self._delete(f"/autopartes/{id}")
