import pytest
from resident.models import UserRole

@pytest.mark.django_db
def test_user_password_change(Normaluser,super_auth_client,client):
    user = UserRole.objects.create(user=Normaluser,is_verfied=False,house_no=104)
    payload = {
        "id":user.id
    }
    response = super_auth_client.post("/api/resident/user-status/", payload)
    assert response.status_code == 200
    payload = {
        "email":"kz251199@gmail.com",
        "password":"Kunal@123"
    }
    response=client.post("/api/user/login/", payload)
    assert response.status_code == 200
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
    payload = {
        "password":"Kunal@123",
        "password2":"Kunal@123"
    }
    response = client.post("/api/user/change-password/", payload)
    assert response.status_code == 200

@pytest.mark.django_db
def test_user_password_change_fail(Normaluser,super_auth_client,client):
    user = UserRole.objects.create(user=Normaluser,is_verfied=False,house_no=104)
    payload = {
        "id":user.id
    }
    response = super_auth_client.post("/api/resident/user-status/", payload)
    assert response.status_code == 200
    payload = {
        "email":"kz251199@gmail.com",
        "password":"Kunal@123"
    }
    response=client.post("/api/user/login/", payload)
    assert response.status_code == 200
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
    payload = {
        "password":"Kunal@23",
        "password2":"Kunal@123"
    }
    response = client.post("/api/user/change-password/", payload)
    assert response.status_code == 400

@pytest.mark.django_db
def test_user_password_same_change_fail(Normaluser,super_auth_client,client):
    user = UserRole.objects.create(user=Normaluser,is_verfied=False,house_no=104)
    payload = {
        "id":user.id
    }
    response = super_auth_client.post("/api/resident/user-status/", payload)
    assert response.status_code == 200
    payload = {
        "email":"kz251199@gmail.com",
        "password":"Kunal@123"
    }
    response=client.post("/api/user/login/", payload)
    assert response.status_code == 200
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
    payload = {
        "password":"Kunal123",
        "password2":"Kunal123"
    }
    response = client.post("/api/user/change-password/", payload)
    assert response.status_code == 400

@pytest.mark.django_db
def test_user_password_cap_check_pass(Normaluser,super_auth_client,client):
    user = UserRole.objects.create(user=Normaluser,is_verfied=False,house_no=104)
    payload = {
        "id":user.id
    }
    response = super_auth_client.post("/api/resident/user-status/", payload)
    assert response.status_code == 200
    payload = {
        "email":"kz251199@gmail.com",
        "password":"Kunal@123"
    }
    response=client.post("/api/user/login/", payload)
    assert response.status_code == 200
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
    payload = {
        "password":"kunal123",
        "password2":"kunal123"
    }
    response = client.post("/api/user/change-password/", payload)
    assert response.status_code == 400

@pytest.mark.django_db
def test_user_profile_seen(Normaluser,super_auth_client,client):
    user = UserRole.objects.create(user=Normaluser,is_verfied=False,house_no=104)
    payload = {
        "id":user.id
    }
    response = super_auth_client.post("/api/resident/user-status/", payload)
    assert response.status_code == 200
    payload = {
        "email":"kz251199@gmail.com",
        "password":"Kunal@123"
    }
    response=client.post("/api/user/login/", payload)
    assert response.status_code == 200
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
    payload = {

    }
    response = client.get("/api/user/profile/", payload)
    assert response.status_code == 200

@pytest.mark.django_db
def test_staff_paaword_change(super_auth_client, client):
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
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
    payload ={
        "password":"Kunal@1234",
        "password2":"Kunal@1234"
    }
    response = client.post("/api/user/change-password/", payload)
    assert response.status_code == 200
    payload = {
        "password": "Kunal@12345",
        "password2": "Kunal@12345"
    }
    response = client.post("/api/user/change-password/", payload)
    assert response.status_code == 200

