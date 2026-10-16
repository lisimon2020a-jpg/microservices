import pytest
from students_service.app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_get_students(client):
    """Проверка, что эндпоинт /students возвращает JSON-список"""
    rv = client.get('/students')
    assert rv.status_code == 200
    assert isinstance(rv.json, list)
    assert len(rv.json) > 0
    assert 'fullName' in rv.json[0]