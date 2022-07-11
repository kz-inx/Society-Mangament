import pytest
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.mark.django_db
class APIUSERLOGiN:
    def test_user_login(self, api_client):
        payload ={
            "commondata": {
                "email": "kunalzaveri10111@gmail.com",
                "name": "Vedhanai Shah",
                "password": "Kunal@123"
            },
            "userdata": {
                "house_no": "105"
            }
        }
        url = reverse('login-url')
        response = api_client.post(url, data=payload)
        assert response.status_code == 200

    def test_password_val(self, api_client):
        payload = {
            "commondata": {
                "email": "kunalzaveri10111@gmail.com",
                "name": "Vedhanai Shah",
                "password": "Kunal123"
            },
            "userdata": {
                "house_no": "105"
            }
        }
        url = reverse('login-url')
        response = api_client.post(url, data=payload)
        assert response.status_code == 400


