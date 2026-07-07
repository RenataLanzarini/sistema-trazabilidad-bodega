from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.dependencies.database import get_db
from app.core.security import hash_password
from app.database.base import Base
from app.main import app
from app.models.bodega import Bodega
from app.models.rol import Rol
from app.models.usuario import Usuario
import app.models as _models  # noqa: F401


@pytest.fixture(scope="session")
def test_environment() -> str:
    return "testing"


@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(test_engine) -> Generator[Session, None, None]:
    connection = test_engine.connect()
    transaction = connection.begin()
    session_factory = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=connection,
    )
    session = session_factory()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def bodega(db_session: Session) -> Bodega:
    bodega = Bodega(nombre="Bodega Test", identificacion_fiscal="TEST-1")
    db_session.add(bodega)
    db_session.flush()
    return bodega


def _crear_rol(db_session: Session, nombre: str) -> Rol:
    rol = Rol(nombre=nombre, activo=True)
    db_session.add(rol)
    db_session.flush()
    return rol


@pytest.fixture
def rol_administrador(db_session: Session) -> Rol:
    return _crear_rol(db_session, "Administrador")


@pytest.fixture
def rol_administrador_duenio(db_session: Session) -> Rol:
    return _crear_rol(db_session, "Administrador/Dueño")


@pytest.fixture
def rol_enologo(db_session: Session) -> Rol:
    return _crear_rol(db_session, "Enólogo")


@pytest.fixture
def rol_operario(db_session: Session) -> Rol:
    return _crear_rol(db_session, "Operario")


def _crear_usuario(
    db_session: Session,
    *,
    bodega: Bodega,
    rol: Rol,
    nombre: str,
    email: str,
    password: str = "clave-segura",
    activo: bool = True,
) -> Usuario:
    usuario = Usuario(
        bodega_id=bodega.id,
        rol_id=rol.id,
        nombre=nombre,
        email=email,
        password_hash=hash_password(password),
        activo=activo,
    )
    db_session.add(usuario)
    db_session.flush()
    return usuario


@pytest.fixture
def usuario_admin(db_session: Session, bodega: Bodega, rol_administrador: Rol) -> Usuario:
    return _crear_usuario(
        db_session,
        bodega=bodega,
        rol=rol_administrador,
        nombre="Admin Test",
        email="admin@example.com",
    )


@pytest.fixture
def usuario_enologo(db_session: Session, bodega: Bodega, rol_enologo: Rol) -> Usuario:
    return _crear_usuario(
        db_session,
        bodega=bodega,
        rol=rol_enologo,
        nombre="Enologo Test",
        email="enologo@example.com",
    )


@pytest.fixture
def usuario_operario(db_session: Session, bodega: Bodega, rol_operario: Rol) -> Usuario:
    return _crear_usuario(
        db_session,
        bodega=bodega,
        rol=rol_operario,
        nombre="Operario Test",
        email="operario@example.com",
    )


@pytest.fixture
def usuario_inactivo(db_session: Session, bodega: Bodega, rol_administrador: Rol) -> Usuario:
    return _crear_usuario(
        db_session,
        bodega=bodega,
        rol=rol_administrador,
        nombre="Inactivo Test",
        email="inactivo@example.com",
        activo=False,
    )


def _auth_headers(client: TestClient, email: str, password: str = "clave-segura") -> dict[str, str]:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_headers_admin(client: TestClient, usuario_admin: Usuario) -> dict[str, str]:
    return _auth_headers(client, usuario_admin.email)


@pytest.fixture
def auth_headers_enologo(client: TestClient, usuario_enologo: Usuario) -> dict[str, str]:
    return _auth_headers(client, usuario_enologo.email)


@pytest.fixture
def auth_headers_operario(client: TestClient, usuario_operario: Usuario) -> dict[str, str]:
    return _auth_headers(client, usuario_operario.email)
