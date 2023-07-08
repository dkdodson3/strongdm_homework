import pytest
from strongdm import BadRequestError, AlreadyExistsError

from tests.conftest import name_values, accepted_punctuation_failures, punctuation_list, unicode_whitespace_characters


@pytest.mark.parametrize("punc", punctuation_list)
def test_add_service_account_with_punctuation(client, service_account, punc):
    service_account_response = None
    service_account.name = f"{service_account.name}{punc}"
    try:
        service_account_response = client.accounts.create(service_account, timeout=30)
    except BadRequestError as e:
        if punc not in accepted_punctuation_failures:
            e.msg = f"{e.msg}: {service_account.name}"
            raise e
    finally:
        if service_account_response:
            client.accounts.delete(service_account_response.account.id)


@pytest.mark.parametrize("description, name_value, should_pass", name_values)
def test_add_service_accounts_with_different_values(client, service_account, description, name_value, should_pass):
    service_account_response = None
    service_account.name = name_value
    try:
        service_account_response = client.accounts.create(service_account, timeout=30)
    except Exception as e:  # BadRequestError, InternalError
        if should_pass:
            e.msg = f"{e.msg}: {service_account.name}"
            raise e
    finally:
        if service_account_response:
            client.accounts.delete(service_account_response.account.id)


@pytest.mark.parametrize("description, unicode_value", unicode_whitespace_characters)
def test_add_service_accounts_with_unicode_values(client, service_account, description, unicode_value):
    service_account_response = None
    service_account.name = f"a_{unicode_value}{service_account.name}"
    try:
        service_account_response = client.accounts.create(service_account, timeout=30)
    except Exception as e:  # BadRequestError, InternalError
        e.msg = f"{e.msg}: {service_account.name}"
        raise e
    finally:
        if service_account_response:
            client.accounts.delete(service_account_response.account.id)


def test_add_service_account_with_same_name(client, service_account):
    service_account_response = None
    try:
        service_account_response = client.accounts.create(service_account, timeout=30)
        service_account_response2 = client.accounts.create(service_account, timeout=30)
        raise Exception(f"Service Account with the same name of '{service_account.name}' should not be allowed to be created")
    except AlreadyExistsError as e:
        pass
    finally:
        if service_account_response:
            client.accounts.delete(service_account_response.account.id)