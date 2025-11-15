class FakeRepo:
    def get_all(self, db=None):
        return [
            {"id": 1, "nombre": "Evento prueba"},
            {"id": 2, "nombre": "Evento demo"}
        ]
