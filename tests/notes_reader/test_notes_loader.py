from app.notes_reader.notes_loader import NotesLoader


def test_tags_are_normalized():
    tags = ['python', '#pytest', '#python', 'Python', ' docker']

    nl = NotesLoader('.', tags)

    assert nl.tags == {'#python', '#pytest', '#docker'}



