import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_signup_success(client):
    response = client.post(reverse('signup'), {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'TestPassword123',
        'confirm_password': 'TestPassword123',
        'terms': True,
    })

    # Check redirect or response code
    assert response.status_code in [200, 302]

    # Check user created
    user_exists = User.objects.filter(username='testuser').exists()
    assert user_exists

@pytest.mark.django_db
def test_signup_password_mismatch(client):
    response = client.post(reverse('signup'), {
        'username': 'testuser2',
        'email': 'testuser2@example.com',
        'password': 'Password123',
        'confirm_password': 'WrongPassword',
        'terms': True,
    })

    assert response.status_code == 200
    assert b"password" in response.content.lower()
    assert not User.objects.filter(username='testuser2').exists()

@pytest.mark.django_db
def test_signup_without_terms(client):
    response = client.post(reverse('signup'), {
        'username': 'testuser3',
        'email': 'testuser3@example.com',
        'password': 'Password123',
        'confirm_password': 'Password123',
        # 'terms' is missing
    })

    assert response.status_code == 200
    assert b"terms" in response.content.lower()
    assert not User.objects.filter(username='testuser3').exists()
