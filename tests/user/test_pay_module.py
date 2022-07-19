import pytest
from resident.models import UserRole

@pytest.mark.django_db
def test_user_pay_maintance_normalpay(Normaluser,super_auth_client,client,auth_client):
    payload = {
        "email":"kz251199@gmail.com",
        "password":"Kunal@123"
    }
    response=auth_client.post("/api/user/login/", payload)
    assert response.status_code == 200
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
    payload = {

    }
    response=client.post("/api/resident/user-pay/", payload)
    assert response.status_code == 200
    # assert "sessionId" in response.data

@pytest.mark.django_db
def test_user_pay_maintance_sub_pay(Normaluser,super_auth_client,client):
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
    response=client.post("/api/resident/user-pay-sub/", payload)
    assert response.status_code == 200

@pytest.mark.django_db
def test_admin_update_maintance(super_auth_client,client):
    payload = {
        "amount_pay": 3500
    }
    response=super_auth_client.put("/api/resident/admin-update-amount/", payload)
    assert response.status_code == 200

@pytest.mark.django_db
def test_admin_update_maintance_fail(super_auth_client,client):
    payload = {

    }
    response=super_auth_client.put("/api/resident/admin-update-amount/", payload)
    assert response.status_code == 400

@pytest.mark.django_db
def test_user_pay_maintance_pay(Normaluser,super_auth_client,client):
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
    response=client.post("/api/resident/user-pay/", payload)
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_pay_maintance_pay_reattempt(Normaluser,super_auth_client,client, auth_client):
    payload = {
        "email":"kz251199@gmail.com",
        "password":"Kunal@123"
    }
    response=auth_client.post("/api/user/login/", payload)
    assert response.status_code == 200
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
    response=auth_client.post("/api/resident/user-pay/")
    assert response.status_code == 200
    response = super_auth_client.get("/api/resident/admin-see-records/?month=07")
    assert response.status_code == 200
    response =auth_client.get("/api/resident/admin-see-records/?month=07")
    assert response.status_code == 403





