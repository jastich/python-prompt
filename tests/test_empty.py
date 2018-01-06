import builtins
import getpass

import pytest

import prompt

@pytest.fixture(autouse=True)
def input_empty(monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda prompt: "")
    monkeypatch.setattr(getpass, "getpass", lambda prompt: "")


def test_character():
    assert prompt.character(empty=True) is None
    assert prompt.character(default='c') is 'c'


def test_email():
    assert prompt.email(empty=True) is None
    assert prompt.email(default='foo@test.com') is 'foo@test.com'


def test_integer():
    assert prompt.integer(empty=True) is None
    assert prompt.integer(default=1) is 1


def test_real():
    assert prompt.real(empty=True) is None
    assert prompt.real(default=1.0) is 1.0


def test_regex():
    assert prompt.regex("foo", empty=True) is None
    assert prompt.regex("foo", default="foo").group(0) == 'foo'


def test_secret():
    assert prompt.secret(empty=True) is None
    assert prompt.secret(default='shh') is 'shh'


def test_string():
    assert prompt.string(empty=True) is None
    assert prompt.string(default='hi') is 'hi'


def test_choice():
    choices = (1, 2)
    assert prompt.choice(choices, empty=True) is None
    assert prompt.choice(choices, default=1) is 1


def test_boolean():
    assert prompt.boolean(default=True)
    assert not prompt.boolean(default=False)
