import pytest
from resident.models import UserRole
from compliant.models import UserCompliant
from django.core import mail

from tests.conftest import Normaluser


@pytest.mark.django_db
def test_user_file_compliant(super_auth_client, client,Normaluser):
    user = UserRole.objects.create(user=Normaluser, is_verfied=False, house_no=104)
    payload = {
        "id": user.id
    }
    response = super_auth_client.post("/api/resident/user-status/", payload)
    assert response.status_code == 200
    payload = {
        "email": "kz251199@gmail.com",
        "password": "Kunal@123"
    }
    response = client.post("/api/user/login/", payload)
    assert response.status_code == 200
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
    email_list = ['kunalzaveri11@gmail.com', 'kz251199@gmail.com', 'azhar.inexture@gmail.com']
    payload = {
        "title": "Water is not coming at my home",
        "subject": "From last two days water is not coming properly at my home"
    }
    response = client.post("/api/compliant/compliant/", payload)
    assert response.status_code == 201
    assert 1 == len(mail.outbox)
    assert mail.outbox[0].subject, 'Water is not coming at my home'

@pytest.mark.django_db
def test_user_file_compliant_fail(super_auth_client, client,Normaluser):
    user = UserRole.objects.create(user=Normaluser, is_verfied=False, house_no=104)
    payload = {
        "id": user.id
    }
    response = super_auth_client.post("/api/resident/user-status/", payload)
    assert response.status_code == 200
    payload = {
        "email": "kz251199@gmail.com",
        "password": "Kunal@123"
    }
    response = client.post("/api/user/login/", payload)
    assert response.status_code == 200
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
    email_list = ['kunalzaveri11@gmail.com', 'kz251199@gmail.com', 'azhar.inexture@gmail.com']
    payload = {

    }
    response = client.post("/api/compliant/compliant/", payload)
    assert response.status_code == 400
    assert 0 == len(mail.outbox)

@pytest.mark.django_db
def test_user_file_compliant_fail_login(super_auth_client, client,Normaluser):
    user = UserRole.objects.create(user=Normaluser, is_verfied=False, house_no=104)
    payload = {
        "id": user.id
    }
    response = super_auth_client.post("/api/resident/user-status/", payload)
    assert response.status_code == 200
    payload = {
        "email": "kz251199@gmail.com",
        "password": "Kuna123"
    }
    response = client.post("/api/user/login/", payload)
    assert response.status_code == 404
    token = {
        "access":"Kunal@12334"
    }
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token['access'])
    email_list = ['kunalzaveri11@gmail.com', 'kz251199@gmail.com', 'azhar.inexture@gmail.com']
    payload = {

    }
    response = client.post("/api/compliant/compliant/", payload)
    assert response.status_code == 401
    assert 0 == len(mail.outbox)

@pytest.mark.django_db
def test_admin_see_notify(Normaluser,super_auth_client,client):
    user = UserRole.objects.create(user=Normaluser, is_verfied=False, house_no=104)
    payload = {
        "id": user.id
    }
    response = super_auth_client.post("/api/resident/user-status/", payload)
    assert response.status_code == 200
    payload = {
        "email": "kz251199@gmail.com",
        "password": "Kunal@123"
    }
    response = client.post("/api/user/login/", payload)
    assert response.status_code == 200
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
    email_list = ['kunalzaveri11@gmail.com', 'kz251199@gmail.com', 'azhar.inexture@gmail.com']
    payload = {
        "title": "Water is not coming at my home",
        "subject": "From last two days water is not coming properly at my home"
    }
    response = client.post("/api/compliant/compliant/", payload)
    assert response.status_code == 201
    assert 1 == len(mail.outbox)
    assert mail.outbox[0].subject, 'Water is not coming at my home'

    response = super_auth_client.get("/api/compliant/see-compliant/")
    assert response.status_code == 200

@pytest.mark.django_db
def test_admin_see_notify_fail(Normaluser,super_auth_client,client):
    user = UserRole.objects.create(user=Normaluser, is_verfied=False, house_no=104)
    payload = {
        "id": user.id
    }
    response = super_auth_client.post("/api/resident/user-status/", payload)
    assert response.status_code == 200
    payload = {
        "email": "kz251199@gmail.com",
        "password": "Kunal@123"
    }
    response = client.post("/api/user/login/", payload)
    assert response.status_code == 200
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
    email_list = ['kunalzaveri11@gmail.com', 'kz251199@gmail.com', 'azhar.inexture@gmail.com']
    payload = {
        "title": "Water is not coming at my home",
        "subject": "From last two days water is not coming properly at my home"
    }
    response = client.post("/api/compliant/compliant/", payload)
    assert response.status_code == 201
    assert 1 == len(mail.outbox)
    assert mail.outbox[0].subject, 'Water is not coming at my home'

    response = client.get("/api/compliant/see-compliant/")
    assert response.status_code == 403

@pytest.mark.django_db
def test_admin_solve_complain(auth_client,super_auth_client,client, Normaluser):
    user_id = Normaluser.user_data.get().id
    payload = {
        "id": user_id
    }
    response = super_auth_client.post("/api/resident/user-status/", payload)
    assert response.status_code == 400
    payload = {
        "email": "kz251199@gmail.com",
        "password": "Kunal@123"
    }
    response = client.post("/api/user/login/", payload)
    assert response.status_code == 200
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
    payload = {
        "title": "Water is not coming at my home",
        "subject": "From last two days water is not coming properly at my home"
    }
    response = auth_client.post("/api/compliant/compliant/", payload)
    assert response.status_code == 201
    assert 1 == len(mail.outbox)
    assert mail.outbox[0].subject, 'Water is not coming at my home'
    user = UserCompliant.objects.all().only('id')
    print(f"First {user[:1]}")
    user_id = [query.id for query in user]
    print(f"Second {user_id[0]}")
    payload = {
        "id": response.data["id"],
    }
    response = super_auth_client.post("/api/compliant/status-update/", payload)
    assert response.status_code == 200
