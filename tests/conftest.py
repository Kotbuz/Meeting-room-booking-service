import pytest_asyncio

from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.core.roles import UserRole
from app.core.security import hash_password
from app.db.database import Base, get_session
from app.main import app, create_default_admin_user
from app.models.users import UserModel
import app.repositories.user_repository as user_repository


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture()
async def session():
    async with engine.connect() as connection:
        transaction = await connection.begin()

        async with AsyncSession(bind=connection, expire_on_commit=False) as session:
            yield session

        await transaction.rollback()


@pytest_asyncio.fixture()
async def client(session):
    async def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture()
async def admin(session):
    await create_default_admin_user(session)
    admin_user = await user_repository.get_user_by_login(
        session,
        settings.admin_login,
    )
    assert admin_user is not None
    return admin_user


@pytest_asyncio.fixture()
async def admin_token(client, admin):
    login_response = await client.post(
        "/api/auth/login",
        data={
            "username": settings.admin_login,
            "password": settings.admin_password,
        },
    )
    assert login_response.status_code == 200
    return login_response.json()["access_token"]


@pytest_asyncio.fixture()
async def admin_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}


@pytest_asyncio.fixture()
async def user(session):
    new_user = UserModel(
        login="test-user",
        password_hash=hash_password("123456"),
        role=UserRole.USER,
    )
    session.add(new_user)
    await user_repository.save(session)
    await user_repository.refresh(session, new_user)
    return new_user


@pytest_asyncio.fixture()
async def user_token(client, user):
    login_response = await client.post(
        "/api/auth/login",
        data={
            "username": user.login,
            "password": "123456",
        },
    )
    assert login_response.status_code == 200
    return login_response.json()["access_token"]


@pytest_asyncio.fixture()
async def user_headers(user_token):
    return {"Authorization": f"Bearer {user_token}"}
