"""Dictation tests."""

import pytest
from django.http import HttpRequest
from django.contrib.sessions.middleware import SessionMiddleware
from apps.dictation.models import correction


@pytest.fixture
def mock_session(mocker):
    request = HttpRequest()
    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(request)
    request.session.save()

    # Mock session
    mock_session = mocker.MagicMock()
    request.session = mock_session

    mock_session = {
        "historic": {
            "revealed_line": [
                {"dict ID": 1, "line": 2, "indexes": [1, 2, 3], "attempts": 0},
                {"dict ID": 1, "line": 3, "indexes": [4, 5], "attempts": 0},
            ]
        },
        "current_dictation": [1],
    }

    # Mock user attribute
    mock_user = mocker.MagicMock()
    mock_user.is_authenticated = True
    request.user = mock_user

    return request


@pytest.mark.django_db
def test_correction_identical_segments(mock_session):
    """Test correction with identical segments."""
    original = "This is a test"
    new = "This is a test"
    dictation_id = 1
    line_number = 1

    result = correction(original, new, dictation_id, line_number, mock_session)

    assert result == ("This is a test", True, 0)


@pytest.mark.django_db
def test_correction_different_dictation_id(mock_session):
    """Test correction with different dictation ID."""
    original = "This is a test"
    new = "This is a best"
    dictation_id = 2
    line_number = 1

    result = correction(original, new, dictation_id, line_number, mock_session)

    assert result[0] == "This is a <span class='spelling'>b</span>est"
    assert result[1] is False
    assert result[2] == 0


@pytest.mark.django_db
def test_correction_with_missing_words(mock_session):
    """Test correction with missing words."""
    original = "This is a test string"
    new = "This is a trest string"
    dictation_id = 1
    line_number = 1

    result = correction(original, new, dictation_id, line_number, mock_session)

    assert (
        result[0]
        == "This is a t<span class='spelling'>r</span><span class='spelling'>e</span><span class='spelling'>s</span><span class='spelling'>t</span> ******"
    )
    assert result[1] is False
    assert result[2] == 0


@pytest.mark.django_db
def test_correction_exact_match(mock_session):
    """Test correction with exact match."""
    original = "This is a test string"
    new = "This is a test string"
    dictation_id = 1
    line_number = 1

    result = correction(original, new, dictation_id, line_number, mock_session)

    assert result[0] == "This is a test string"
    assert result[1] is True
    assert result[2] == 0
