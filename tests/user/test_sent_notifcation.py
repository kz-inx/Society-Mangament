import pytest
from notifcations.models import Notifcation
from resident.models import UserRole
from django.core import mail


@pytest.mark.django_db
def test_user_email_sent_all(Normaluser,super_auth_client,client):
    print("cool............")
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
    email_list = ['kunalzaveri11@gmail.com','kz251199@gmail.com']
    payload = {
        "title": "Pay maintance",
        "message": "Pay your maintance before the dateline..."
    }
    response = super_auth_client.post("/api/notify/sendall/", payload)
    assert response.status_code == 201
    assert 1 == len(mail.outbox)
    assert mail.outbox[0].subject, 'Pay maintance'

@pytest.mark.django_db
def test_user_email_sent_fail_all(Normaluser,super_auth_client,client):
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
    email_list = ['kunalzaveri11@gmail.com','kz251199@gmail.com']
    payload = {

    }
    response = super_auth_client.post("/api/notify/sendall/", payload)
    assert response.status_code == 400
    assert 0 == len(mail.outbox)

@pytest.mark.django_db
def test_user_email_sent_ind(Normaluser,super_auth_client,client):
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
    email_list = ['kunalzaveri11@gmail.com']
    payload = {
        "title": "Pay maintance",
        "message": "Pay your maintance before the dateline...",
        "house_no":104
    }
    response = super_auth_client.post("/api/notify/sendoneuser/", payload)
    assert response.status_code == 201
    assert 1 == len(mail.outbox)
    assert mail.outbox[0].subject, 'Pay maintance'

@pytest.mark.django_db
def test_user_email_sent_ind_fail(Normaluser,super_auth_client,client):
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
    email_list = ['kunalzaveri11@gmail.com']
    payload = {

    }
    response = super_auth_client.post("/api/notify/sendoneuser/", payload)
    assert response.status_code == 400
    assert 0 == len(mail.outbox)

@pytest.mark.django_db
def test_user_see_notify(Normaluser,super_auth_client,client):
    print("cool")
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
    email_list = ['kunalzaveri11@gmail.com','kz251199@gmail.com']
    payload = {
        "title": "Pay maintance",
        "message": "Pay your maintance before the dateline..."
    }
    response = super_auth_client.post("/api/notify/sendall/", payload)
    assert response.status_code == 201
    assert 1 == len(mail.outbox)
    assert mail.outbox[0].subject, 'Pay maintance'
    payload = {
        "email": "kz251199@gmail.com",
        "password": "Kunal@123"
    }
    response = client.post("/api/user/login/", payload)
    assert response.status_code == 200
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
    payload = {

    }
    response = client.get("/api/notify/see-notify")
    assert response.status_code == 200

@pytest.mark.django_db
def test_user_see_notify_fail(Normaluser,super_auth_client,client):
    print("cool")
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
    email_list = ['kunalzaveri11@gmail.com','kz251199@gmail.com']
    payload = {
        "title": "Pay maintance",
        "message": "Pay your maintance before the dateline..."
    }
    response = super_auth_client.post("/api/notify/sendall/", payload)
    assert response.status_code == 201
    assert 1 == len(mail.outbox)
    assert mail.outbox[0].subject, 'Pay maintance'
    payload = {
        "email": "kz251199@gmail.com",
        "password": "Kunal123"
    }
    response = client.post("/api/user/login/", payload)
    assert response.status_code == 404
    token = {
        "access":"ABC"
    }
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token['access'])
    payload = {

    }
    response = client.get("/api/notify/see-notify")
    assert response.status_code == 401

