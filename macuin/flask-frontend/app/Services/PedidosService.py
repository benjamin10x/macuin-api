from app.Services.BaseService import BaseService


class PedidosService(BaseService):
    def all(self):
        return self._get("/pedidos/")
