import pytest
from user.models import User
from resident.models import UserRole


@pytest.mark.django_db
def test_user_reg_success_admin_login(client):
    payload ={
            "email": "kunalzaveri10111@gmail.com",
            "name": "Vedhanai Shah",
            "password": "Kunal@123",
            "house_no": "105",

            }
    response = client.post("/api/user/register-user/", payload)
    assert response.status_code == 201
    user_id = User.objects.filter(email=payload["email"]).first().pk
    print(user_id)
    payload = {
        "id": user_id,
    }
    response = client.post("/api/user/new-admin-system/", payload)
    assert response.status_code == 200

@pytest.mark.django_db
def test_user_reg_succes(client):
    payload ={
        "email": "kunalzaveri10111@gmail.com",
        "name": "Vedhanai Shah",
        "password": "Kunal@123",
        "house_no": "105",
    }
    response = client.post("/api/user/register-user/", payload)
    assert response.status_code == 201

@pytest.mark.django_db
def test_user_reg_password_fail(client):
    payload={
        "email":"kunalzaveri11@gmail.com",
        "name":"kunalzaveri",
        "password":"Kunal",
        "house_no":"105"
    }
    response = client.post("/api/user/register-user/", payload)
    data = response.data
    assert response.status_code == 400

@pytest.mark.django_db
def test_user_reg_data_val(client):
    payload = {
        "email":"kunalzaveri11@gmail.com",
        "name":"kush"
    }
    response = client.post("/api/user/register-user/", payload)
    data = response.data
    assert response.status_code == 400
    assert data['password'][0] == "This field is required."



@pytest.mark.django_db
def test_user_login_val(Normaluser,client):
    payload ={
        "email":"kunalzaveri11@gmail.com",
        "password":"Testing@321"
    }
    response = client.post("/api/user/login/", payload)
    assert response.status_code == 404


@pytest.mark.django_db
def test_user_verified(Normaluser,super_auth_client,client):
    user = UserRole.objects.create(user=Normaluser,is_verfied=False,house_no=104)
    payload = {
        "id":user.id
    }
    response = super_auth_client.post("/api/resident/user-status/", payload)
    assert response.status_code == 200




