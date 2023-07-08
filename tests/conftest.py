import random

import pytest
import os
import strongdm

# from typing import Optional
# from pydantic import BaseModel, EmailStr
#
#
# class User(BaseModel):
#     id: Optional[int] = None
#     name: str
#     email: EmailStr


@pytest.fixture(scope="session", name="credentials")
def get_client_credentials_fixture() -> dict:
    creds = {
        "api_access_key": os.getenv("SDM_API_ACCESS_KEY", ""),
        "api_secret": os.getenv("SDM_API_SECRET_KEY", "")
    }

    return creds


@pytest.fixture(name="client")
def get_client_fixture(credentials):
    client = strongdm.Client(**credentials)
    yield client
    pass


def get_user(first: str = None, last: str = None, email_address: str = None):
    if not first:
        first = f"Tacos{random.randint(100000, 999999)}"

    if not last:
        last = f"McMuffin{random.randint(100000, 999999)}"

    if not email_address:
        email_address = f"{first}_{last}_{random.randint(100000, 999999)}@eyepaste.com"

    return strongdm.User(email=email_address, first_name=first, last_name=last,
)


@pytest.fixture(name="user")
def buser_fixture() -> strongdm.User:
    return get_user()


@pytest.fixture(name="service_account")
def service_fixture() -> strongdm.Service:
    return strongdm.Service(name=f"Apple_{random.randint(100000000, 999999999)}")


punctuation_list = list("~!@#$%^&*()_+|}{[]\":;'<>? `/.,")
accepted_punctuation_failures = ["\"", "<", ">"]

name_values = [
    ("Normal Name", "John Doe", True),
    ("No Name", "", False),
    ("Space for Name", " ", False),
    ("Min characters for Name", "a", True),
    ("Max characters for Name", "a" * 1024, True),
    ("Over Max characters for Name", "a" * 1025, True),  # This should fail but not in this way so I marked it as True so we can see it...
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