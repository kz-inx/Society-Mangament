import pytest
from visitors.models import VisitorsSociety
from datetime import datetime
datetime.now()

@pytest.mark.django_db
def test_registior_visitors_staff(super_auth_client,auth_client,client):
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
    payload = {
        "password":"Kunal@12345",
        "password2":"Kunal@12345"
    }
    response = client.post("/api/user/change-password/", payload)
    assert response.status_code == 200
    payload = {
        "email": "ramesh.inexture+azhar@gmail.com",
        "password": "Kunal@12345",
    }
    response = client.post("/api/user/login/", payload)
    assert response.status_code == 200
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
    payload = {
        "name": "Het Suthar",
        "phone_number": "+919601031518",
        "house_no": "105"
    }
    response = client.post("/api/visitors/register-user/", payload)
    assert response.status_code == 201

@pytest.mark.django_db
def test_user_watch_visitors(super_auth_client,auth_client,client):
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
    payload = {
        "password":"Kunal@12345",
        "password2":"Kunal@12345"
    }
    response = client.post("/api/user/change-password/", payload)
    assert response.status_code == 200
    payload = {
        "email": "ramesh.inexture+azhar@gmail.com",
        "password": "Kunal@12345",
    }
    response = client.post("/api/user/login/", payload)
    assert response.status_code == 200
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
    payload = {
        "name": "Het Suthar",
        "phone_number": "+919601031518",
        "house_no": "104"
    }
    response = client.post("/api/visitors/register-user/", payload)
    assert response.status_code == 201
    response = auth_client.get("/api/visitors/see-visitors/")
    assert response.status_code == 200

@pytest.mark.django_db
def test_user_update_status(super_auth_client,auth_client,client):
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
    payload = {
        "password":"Kunal@12345",
        "password2":"Kunal@12345"
    }
    response = client.post("/api/user/change-password/", payload)
    assert response.status_code == 200
    payload = {
        "email": "ramesh.inexture+azhar@gmail.com",
        "password": "Kunal@12345",
    }
    response = client.post("/api/user/login/", payload)
    assert response.status_code == 200
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
    payload = {
        "name": "Het Suthar",
        "phone_number": "+919601031518",
        "house_no": "104"
    }
    response = client.post("/api/visitors/register-user/", payload)
    assert response.status_code == 201

    response = auth_client.get("/api/visitors/see-visitors/")
    assert response.status_code == 200
    user = VisitorsSociety.objects.all().only('id')
    user_id = [query.id for query in user]
    payload = {
        "id": user_id[0],
        "is_status": "Accepted"
    }
    response = auth_client.post("/api/visitors/update-status/",payload)
    assert response.status_code == 200

@pytest.mark.django_db
def test_user_update_status_fail(super_auth_client,auth_client,client):
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
    payload = {
        "password":"Kunal@12345",
        "password2":"Kunal@12345"
    }
    response = client.post("/api/user/change-password/", payload)
    assert response.status_code == 200
    payload = {
        "email": "ramesh.inexture+azhar@gmail.com",
        "password": "Kunal@12345",
    }
    response = client.post("/api/user/login/", payload)
    assert response.status_code == 200
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
    payload = {
        "name": "Het Suthar",
        "phone_number": "+919601031518",
        "house_no": "104"
    }
    response = client.post("/api/visitors/register-user/", payload)
    assert response.status_code == 201

    response = auth_client.get("/api/visitors/see-visitors/")
    assert response.status_code == 200
    user = VisitorsSociety.objects.all().only('id')
    user_id = [query.id for query in user]
    payload = {
        "id": user_id[0],
        "is_status": "Accepted"
    }
    response = auth_client.post("/api/visitors/update-status/",payload)
    assert response.status_code == 200
    payload = {
        "id": user_id[0],
        "is_status": "Accepted"
    }
    response = auth_client.post("/api/visitors/update-status/", payload)
    assert response.status_code == 404

@pytest.mark.django_db
def test_staff_see_all_visistors(super_auth_client,client,auth_client):
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
    payload = {
        "password": "Kunal@12345",
        "password2": "Kunal@12345"
    }
    response = client.post("/api/user/change-password/", payload)
    assert response.status_code == 200
    payload = {
        "email": "ramesh.inexture+azhar@gmail.com",
        "password": "Kunal@12345",
    }
    response = client.post("/api/user/login/", payload)
    assert response.status_code == 200
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
    payload = {
        "name": "Het Suthar",
        "phone_number": "+919601031518",
        "house_no": "105"
    }
    response = client.post("/api/visitors/register-user/", payload)
    assert response.status_code == 201
    response = client.get("/api/visitors/staff-see-visitors/")
    assert response.status_code == 200
    response = auth_client.get("/api/visitors/user-see-visitors/")
    assert response.status_code == 200
    response = client.get("/api/visitors/user-see-visitors/")
    assert response.status_code == 400
    response = super_auth_client.get("/api/visitors/staff-see-visitors/")
    assert response.status_code == 400

@pytest.mark.django_db
def test_reg_daily_vistiors_staff_see(super_auth_client, client):
    with open('media/profile_pics/3.jpeg', 'rb') as profile_pics:
        payload = {
            "serial_id":"AB123",
            "name":"Misha",
            "profile_pics":profile_pics,
            "phone_number":"+919601031518",
            "addharcard_number":"123456781234"
        }
        response = super_auth_client.post("/api/visitors/daily-visitors-register/", payload)
        assert response.status_code == 201
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
        payload = {
            "password": "Kunal@12345",
            "password2": "Kunal@12345"
        }
        response = client.post("/api/user/change-password/", payload)
        assert response.status_code == 200
        payload = {
            "email": "ramesh.inexture+azhar@gmail.com",
            "password": "Kunal@12345",
        }
        response = client.post("/api/user/login/", payload)
        assert response.status_code == 200
        response = client.get("/api/visitors/daily-visitors-verify/AB123/")
        assert response.status_code == 202


@pytest.mark.django_db
def test_reg_daily_vistiors_staff_fai(super_auth_client, client):
    with open('media/profile_pics/3.jpeg', 'rb') as profile_pics:
        payload = {
            "serial_id": "AB123",
            "name": "Misha",
            "profile_pics": profile_pics,
            "phone_number": "+919601031518",
            "addharcard_number": "123456781234"
        }
        response = super_auth_client.post("/api/visitors/daily-visitors-register/", payload)
        assert response.status_code == 201
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
        response = client.get("/api/visitors/daily-visitors-verify/AB123/")
        assert response.status_code == 400

@pytest.mark.django_db
def test_reg_daily_vistiors_user_fail(super_auth_client, client, auth_client):
    with open('media/profile_pics/3.jpeg', 'rb') as profile_pics:
        payload = {
            "serial_id": "AB123",
            "name": "Misha",
            "profile_pics": profile_pics,
            "phone_number": "+919601031518",
            "addharcard_number": "123456781234"
        }
        response = super_auth_client.post("/api/visitors/daily-visitors-register/", payload)
        assert response.status_code == 201
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
            "email": "kz251199@gmail.com",
            "password": "Kunal@123"
        }
        response = auth_client.post("/api/user/login/", payload)
        assert response.status_code == 200
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
        response = client.get("/api/visitors/daily-visitors-verify/AB123/")
        assert response.status_code == 400


