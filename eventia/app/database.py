from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Detectar ambiente de pruebas
ENV = os.getenv("ENV")

if ENV == "TEST":
    # Base de datos SQLite para pruebas unitarias
    DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    # Base de datos real MySQL
    DATABASE_URL = "mysql+pymysql://root:@localhost/eventia_core"
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

