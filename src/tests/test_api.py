import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import app_settings
from db.db import Base, get_session
from main import app


SQLALCHEMY_DATABASE_URL = 'postgresql+asyncpg://test:test@localhost:5432/test'
TEST_URL_1 = 'https://ya.ru/'
TEST_URL_2 = 'https://yandex.ru/'


async def override_get_session() -> AsyncSession:
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(scope='session')
def get_client():
    client = TestClient(app)
    return client


def test_url_creation(get_client):
    data = {
        'original_url': TEST_URL_1
    }
    response = get_client.post(app.url_path_for('create_short_url'), json=data)

    assert response.status_code == 201
    response_message = {
        'short_url': f'{app_settings.short_url_pattern}1',
        'original_url': TEST_URL_1
    }
    assert response.json() == response_message


def test_bulk_creation(get_client):
    data = [
        {
            'original_url': TEST_URL_1
        },
        {
            'original_url': TEST_URL_2
        }
    ]

    response = get_client.post(
        app.url_path_for('bulk_create_short_url'), json=data
    )

    assert response.status_code == 201
    response_message = [
        {
            'short_url': f'{app_settings.short_url_pattern}1',
            'short_id': 1
        },
        {
            'short_url': f'{app_settings.short_url_pattern}2',
            'short_id': 2
        }
    ]
    assert response.json() == response_message
