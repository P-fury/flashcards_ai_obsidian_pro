import os
import re
from datetime import datetime

import pytest

from app.models.note_models import Note


def test_empty_title_raise_value_error():
    print(os.getenv("TESTS"))  # check for test environment
    with pytest.raises(ValueError, match="Title must be a not-empty string."):
        Note(
            title="",
            content="Note content.",
            tags={"python", "pytest"},
            updated_at=datetime.now(),
        )


def test_empty_content_rise_value_error():
    with pytest.raises(ValueError, match="Content must be a not-empty string."):
        Note(title="Title", content="", tags={"python"}, updated_at=datetime.now())


def test_empty_tags_rise_value_error():
    with pytest.raises(ValueError, match=re.escape("Tags: set() must be a non-empty set.")):
        Note(title="Title", content="Note content", tags=set(), updated_at=datetime.now())


def test_tags_with_empty_values_rise_value_error():
    with pytest.raises(ValueError, match=re.escape("Tags: set() must be a non-empty set.")):
        Note(title="Title", content="Note content", tags={"", "  "}, updated_at=datetime.now())


def test_tags_are_striped():
    note = Note(title="Title", content="Note content", tags={"python  ", "  pytest"}, updated_at=datetime.now())
    assert note.tags == {"python", "pytest"}


def test_tags_are_lowercase():
    note = Note(title="Title", content="Note content", tags={"Python", "  pyTest"}, updated_at=datetime.now())
    assert note.tags == {"python", "pytest"}


def test_empty_tags_are_removed():
    note = Note(title="Title", content="Note content", tags={"python", "  pytest", "", "  "}, updated_at=datetime.now())
    assert note.tags == {"python", "pytest"}
