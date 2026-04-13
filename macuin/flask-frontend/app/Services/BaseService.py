import os
import requests


class BaseService:
    def __init__(self):
        self.api_url = os.getenv("API_URL", "http://api:8000/v1")

    def _get(self, endpoint):
        try:
            r = requests.get(f"{self.api_url}{endpoint}", timeout=5)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(f"[API ERROR GET] {endpoint}: {e}")
            return []

    def _post(self, endpoint, data):
        try:
            r = requests.post(f"{self.api_url}{endpoint}", json=data, timeout=5)
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

    def _put(self, endpoint, data):
        try:
            r = requests.put(f"{self.api_url}{endpoint}", json=data, timeout=5)
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

    def _delete(self, endpoint):
        try:
            r = requests.delete(f"{self.api_url}{endpoint}", timeout=5)
            r.raise_for_status()
            return True, None
        except Exception as e:
            return False, str(e)
