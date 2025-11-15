import sys
import os

# Asegurar acceso al paquete principal
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base
from app.main import app
from app.database import get_db


# -----------------------------
# Configurar DB de prueba (SQLite en memoria)
# -----------------------------
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@pytest.fixture(scope="function")
def test_db():
    # Crear tablas
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


# -----------------------------
# Fixture para TestClient
# -----------------------------
@pytest.fixture(scope="function")
def client(test_db):

    # Sobrescribir correctamente la dependencia get_db
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    # Limpiar override después
    app.dependency_overrides.clear()


# -----------------------------
# Fixture fake_redis
# -----------------------------
@pytest.fixture
def fake_redis():
    class FakeRedis:
        def __init__(self):
            self.store = {}

        def get(self, key):
            value = self.store.get(key)
            if value is None:
                return None
            return value  # bytes, igual que redis real

        def set(self, key, value, ex=None):
            # value debe guardarse como bytes
            if isinstance(value, str):
                value = value.encode("utf-8")
            self.store[key] = value

        def delete(self, key):
            self.store.pop(key, None)

    return FakeRedis()


