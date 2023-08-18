import pytest


@pytest.fixture
def user_data():
    return {
        "name": "ФОП Джонсонюк Борис",
        "username": "boris",
        "password": "boris1234"
    }
