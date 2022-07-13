import pytest
from user.models import User

@pytest.mark.django_db
def test_staff_regs_admin(super_auth_client, client):
    payload = {
        "rolename":"Watchman"
    }
    response = super_auth_client.post("/api/staff/register-role/", payload)
    assert response.status_code == 201
    payload ={
        "email": "ramesh.inexture+azhar@gmail.com",
        "name": "ramesh",
        "password": "Kunal@123",
        "role": "1"
    }
    response = super_auth_client.post("/api/user/register-staff/", payload)
    assert response.status_code == 201

@pytest.mark.django_db
def test_staff_login(super_auth_client, client):
    payload = {
        "rolename": "Watchman"
    }
    response = super_auth_client.post("/api/staff/register-role/", payload)
    assert response.status_code == 201
    payload = {
        "email": "ramesh.inexture+azhar@gmail.com",
        "name": "ramesh",
        "password": "Kunal@123",
        "role": response.data['id']
    }
    response = super_auth_client.post("/api/user/register-staff/", payload)
    assert response.status_code == 201

    payload = {
        "email": "ramesh.inexture+azhar@gmail.com",
        "password": "Kunal@123",
    }
    response = client.post("/api/user/login/", payload)
    assert response.status_code == 200
