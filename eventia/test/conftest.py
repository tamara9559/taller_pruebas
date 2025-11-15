import sys
import os

# Agregar la carpeta 'eventia' al path antes de cualquier import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app")))

from app.database import Base
from app.main import app

# -----------------------------
# Configurar DB de prueba
# -----------------------------
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def test_db():
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
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[lambda: None] = override_get_db
    with TestClient(app) as c:
        yield c

# -----------------------------
# Fixture fake_redis
# -----------------------------
@pytest.fixture
def fake_redis():
    class FakeRedis:
        def __init__(self):
            self.store = {}

        def get(self, key):
            return self.store.get(key)

        def set(self, key, value):
            self.store[key] = value

        def delete(self, key):
            self.store.pop(key, None)

    return FakeRedis()
