"""Dictation tests."""

import pytest
from django.http import HttpRequest
from apps.dictation.models import correction


@pytest.fixture
def mock_request():
    """Fixture to create a mock HttpRequest object with a session."""
    request = HttpRequest()

    request.session = {
        "historic": {
            "revealed_line": [
                {"dict ID": 1, "line": 2, "indexes": [1, 2, 3], "attempts": 0},
                {"dict ID": 1, "line": 3, "indexes": [4, 5], "attempts": 0},
            ]
        },
        "current_dictation": [1],
    }
    return request


def test_correction_identical_segments(mock_request):
    original = "This is a test"
    new = "This is a test"
    dictation_id = 1
    line_number = 1

    result = correction(original, new, dictation_id, line_number, mock_request)

    assert result == ("This is a test", True, 0)


def test_correction_different_dictation_id(mock_request):
    original = "This is a test"
    new = "This is a best"
    dictation_id = 2
    line_number = 1

    result = correction(original, new, dictation_id, line_number, mock_request)

    assert result[0] == "This is a <span class='spelling'>b</span>est"
    assert result[1] is False
    assert result[2] == 0


def test_correction_with_missing_words(mock_request):
    original = "This is a test string"
    new = "This is a trest string"
    dictation_id = 1
    line_number = 1

    result = correction(original, new, dictation_id, line_number, mock_request)

    assert (
        result[0]
        == "This is a t<span class='spelling'>r</span><span class='spelling'>e</span><span class='spelling'>s</span><span class='spelling'>t</span> ******"
    )
    assert result[1] is False
    assert result[2] == 0


def test_correction_exact_match(mock_request):
    original = "This is a test string"
    new = "This is a test string"
    dictation_id = 1
    line_number = 1

    result = correction(original, new, dictation_id, line_number, mock_request)

    assert result[0] == "This is a test string"
    assert result[1] is True
    assert result[2] == 0
