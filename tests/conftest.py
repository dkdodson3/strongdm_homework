import random

import pytest
import os
import strongdm


# --- Shared Functions ---
def get_user(first: str = None, last: str = None, email_address: str = None) -> strongdm.User:
    """
    Creates a prepopulated strongdm user
    :param first: str
    :param last: str
    :param email_address: str
    :return: strongdm.User
    """
    if not first:
        first = f"Tacos{random.randint(100000, 999999)}"

    if not last:
        last = f"McMuffin{random.randint(100000, 999999)}"

    if not email_address:
        email_address = f"{first}_{last}_{random.randint(100000, 999999)}@eyepaste.com"

    return strongdm.User(email=email_address, first_name=first, last_name=last)


def get_role(name: str = None, access_rules: list = None) -> strongdm.Role:
    """
    Creates a prepopulated strongdm role
    :param name: str
    :param access_rules: list
    :return: strongdm.Role
    """
    if not name:
        name = f"ROLL_{random.randint(100000000, 999999999)}"

    if not access_rules:
        access_rules = list()

    return strongdm.Role(name=name, access_rules=access_rules)


def get_resource_postgres(num: int = None) -> strongdm.Postgres:
    """
    Creates a prepopulated strongdm postgres
    :param num: int
    :return: strongdm.Postgres
    """
    if not num:
        num = random.randint(1000000, 9999999)

    postgres = strongdm.Postgres(
        name=f"Fake Postgres Resource{num}",
        hostname=f"foo{num}.bar.com",
        port=5432,
        username=f"foo{num}",
        password="test123",
        database="foo"
    )

    return postgres


# --- Fixtures ---
@pytest.fixture(scope="session", name="credentials")
def get_client_credentials_fixture() -> dict:
    """
    Gets the api keys from the OS
    :return: dict
    """
    creds = {
        "api_access_key": os.getenv("SDM_API_ACCESS_KEY", ""),
        "api_secret": os.getenv("SDM_API_SECRET_KEY", "")
    }

    return creds


@pytest.fixture(name="client")
def get_client_fixture(credentials) -> strongdm.Client:
    """
    Creates a client
    :return: strongdm.Client
    """
    client = strongdm.Client(**credentials)
    yield client


@pytest.fixture(name="user")
def user_fixture() -> strongdm.User:
    """
    Creates a strongdm user
    :return: strongdm.User
    """
    return get_user()


@pytest.fixture(name="service_account")
def service_fixture() -> strongdm.Service:
    """
    Creates a strongdm service account
    :return: strongdm.Service
    """
    return strongdm.Service(name=f"Apple_{random.randint(100000000, 999999999)}")


@pytest.fixture(name="role")
def role_fixture() -> strongdm.Role:
    """
    Creates a strongdm role
    :return: strongdm.Role
    """
    return get_role()


@pytest.fixture(name="resource_postgres")
def resource_postgres_fixture() -> strongdm.Postgres:
    """
    Creates a strongdm postgres datasource
    :return: strongdm.Postgres
    """
    return get_resource_postgres()


# --- Shared Test Data for Parameterization ---
punctuation_list = list("~!@#$%^&*()_+|}{[]\":;'<>? `/.,")
accepted_punctuation_failures = ["\"", "<", ">"]

name_values = [
    ("Normal Name", "John Doe", True),
    ("No Name", "", False),
    ("Space for Name", " ", False),
    ("Min characters for Name", "a", True),
    ("Max characters for Name", "a" * 1024, True),
    ("Over Max characters for Name", "a" * 1025, True),
    ("Foreign characters in Name", "Ľuboš Bartečko", True),
    ("Chinese characters in Name", "您可以撼動它", True),
    ("HTML in Name", "<a href=”http://cnn.com”>CNN</a>", False),
    ("JavaScript in Name", 'javascript:alert("Danger!");', False),
    ("Null in Name", 'null', False),
]

updated_name_values = [
    ("Normal Name", "foo", True),
    ("No Name", "", False),
    ("Space for Name", " ", False),
    ("Null in Name", 'null', True),
]

email_values = [
    ("Normal Email", "bob@bob.com", True),
    ("Invalid Email", "bob@@bob.com", False),
    ("No Email", None, False),
    ("Null Email", "null", False),
    ("Foreign Characters Email", "Ľuboš_Bartečko@bob.com", True),
    ("Chinese Characters Email", "您可以撼動它@bob.com", True),
]

updated_email_values = [
    ("Normal Email", "bob@bob.com", True),
    ("Invalid Email", "bob@@bob.com", False),
    ("No Email", None, False),
    ("Foreign Characters Email", "Ľuboš_Bartečko@bob.com", True)
]

suspend_values = [
    (True, True),
    (False, False),
    (0, False),
    (1, True),
]

delete_values = [
    ("Good id", "REPLACE_ME", True),
    ("Bad id", "tacos", False),
    ("String int", "123456", False),
    ("String Empty", "", False),
    ("String null", "null", False),
    ("Value None", None, False),
]

unicode_whitespace_characters = [
    ("space", "\u0020"),
    ("character tabulation", "\u0009"),
    ("line feed", "\u000a"),
    ("line tabulation", "\u000b"),
    ("form feed", "\u000c"),
    ("carriage return", "\u000d"),
    ("next line", "\u0085"),
    ("no-break space", "\u00a0"),
    ("ogham space mark", "\u1680"),
    ("mongolian vowel mark", "\u180e"),
    ("en quad", "\u2000"),
    ("em quad", "\u2001"),
    ("en space", "\u2002"),
    ("em space", "\u2003"),
    ("three-per-em space", "\u2004"),
    ("four-per-em space", "\u2005"),
    ("six-per-em space", "\u2006"),
    ("figure space", "\u2007"),
    ("punctuation space", "\u2008"),
    ("thin space", "\u2009"),
    ("hair space", "\u200A"),
    ("line separator", "\u2028"),
    ("paragraph separator", "\u2029"),
    ("narrow no-break space", "\u202f"),
    ("medium mathematical space", "\u205f"),
    ("ideographic space", "\u3000"),
    ("word joiner", "\u2060"),
    ("zero width non-breaking space", "\ufeff")
]
