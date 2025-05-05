import pytest
from django.contrib.auth.models import User
from django.urls import reverse

@pytest.fixture
def create_test_user(db):
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='TestPassword123'
    )
    return user

@pytest.mark.django_db
def test_login_success(client, create_test_user):
    response = client.post(reverse('login'), {
        'username': 'testuser',
        'password': 'TestPassword123',
    })

    # A successful login usually redirects
    assert response.status_code in [200, 302]
    assert '_auth_user_id' in client.session

@pytest.mark.django_db
def test_login_wrong_password(client, create_test_user):
    response = client.post(reverse('login'), {
        'username': 'testuser',
        'password': 'WrongPassword',
    })

    # Form should return an error, no redirect
    assert response.status_code == 200
    assert b"password" in response.content.lower()
    assert '_auth_user_id' not in client.session

@pytest.mark.django_db
def test_login_nonexistent_user(client):
    response = client.post(reverse('login'), {
        'username': 'ghost',
        'password': 'irrelevant',
    })

    assert response.status_code == 200
    assert b"username" in response.content.lower()
    assert '_auth_user_id' not in client.session
