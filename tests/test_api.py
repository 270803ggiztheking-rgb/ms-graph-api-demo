from unittest.mock import patch


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@patch("src.services.user_service.UserService.get_me")
def test_get_me(mock_get_me, client):
    mock_get_me.return_value = {
        "id": "123",
        "displayName": "Test User",
        "mail": "test@example.com",
    }

    response = client.get("/api/v1/users/me")
    assert response.status_code == 200
    assert response.json()["displayName"] == "Test User"


@patch("src.services.mail_service.MailService.get_messages")
def test_get_emails(mock_get_messages, client):
    mock_get_messages.return_value = []
    response = client.get("/api/v1/mail/")
    assert response.status_code == 200
    assert response.json() == []
