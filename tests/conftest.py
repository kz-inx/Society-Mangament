import pytest
from user.models import User
from rest_framework.test import APIClient
from resident.models import UserRole


@pytest.fixture()
def Superuser():
    user = User.objects.create_superuser(email="kunalzaveri11@gmail.com",
                                         name="Kunal Zaveri",
                                         password="Testing@321"
                                         )
    return user


@pytest.fixture()
def Normaluser():
    normaluser = User.objects.create_user(
            email="kz251199@gmail.com",
            name="kunalzaveri",
            password="Kunal@123",
    )
    return normaluser



@pytest.fixture()
def client():
    client = APIClient()
    return client


@pytest.fixture
def refresh_token(Superuser, client):
    payload = {
        "email": "kunalzaveri11@gmail.com",
        "password": "Testing@321",
    }
    response = client.post("/api/user/login/", payload)
    return response.data['refresh']


@pytest.fixture
def super_auth_client(Superuser):
    client = APIClient()
    payload = {
        "email": "kunalzaveri11@gmail.com",
        "password": "Testing@321",
    }
    response = client.post("/api/user/login/", payload)
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
    return client

@pytest.fixture
def auth_client(Normaluser):
    client = APIClient()
    payload = {
        "email": "kz251199@gmail.com",
        "password": "Kunal@123",
    }
    UserRole.objects.create(user=Normaluser, is_verfied=True, house_no=104)
    response = client.post("/api/user/login/", payload)
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
    return client