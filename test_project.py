# Harvard CS50 Python
########################################
# Test functions for final project
# Project name: Authentication App With Rate Limiter
# Creator: Paul Münzner
# pytest test_project.py

import pytest

from project import (
    auth_selection,
    hash_password,
    password_match,
    validate_email_format,
    validate_password_format,
)


def test_auth_selection():
    assert auth_selection("login") == "login"
    assert auth_selection("register") == "register"
    with pytest.raises(ValueError):
        auth_selection("")
        auth_selection("no idea")
        auth_selection("help")


# ----------------- validate_email_format ------------------
# Fixture to provide different email addresses
@pytest.fixture(
    params=[
        "login",
        "name@gmail.com",
        "6657898@xyz.inbox.io",
        "johndoe@yahoo.com",
        "@aol.com",
    ]
)
def email_address(request):
    return request.param


# Use the fixture in a test
def test_validate_email(email_address):
    result = validate_email_format(email_address)
    if "@" in email_address:
        assert result is True
    else:
        assert result is False


# ----------------- test_validate_password ------------------
# Fixture to provide different passwords
@pytest.fixture(
    params=[
        "tooshort",
        "muchmuchtoolongpassword",
        "$^*($$=#^)++",
        "ThkOP98T5rr",
        "T..5+=8T@T6",
        "Test576pazzword",
    ]
)
def password(request):
    return request.param


# Use the fixture in a test
def test_validate_password(password):
    result = validate_password_format(password)
    if not (8 <= len(password) <= 20) or password.isalnum():
        assert result is False
    else:
        assert result is True


# ----------------- test_password_match ------------------
def test_password_match():
    assert (
        password_match("SimplePassword", hash_password(
            "SimplePassword").decode("utf8"))
        is True
    )
    assert (
        password_match(
            "SimplePassword", hash_password("DifferentPassword").decode("utf8")
        )
        is False
    )
    assert (
        password_match(
            "HardPassword8899%$33Tgv!",
            hash_password("HardPassword8899%$33Tgv!").decode("utf8"),
        )
        is True
    )
