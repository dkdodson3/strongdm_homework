import pytest
from strongdm import BadRequestError, AlreadyExistsError, InternalError, NotFoundError

from tests.conftest import name_values, accepted_punctuation_failures, punctuation_list, unicode_whitespace_characters, \
    updated_name_values, suspend_values, delete_values


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
    except (BadRequestError, InternalError) as e:
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
    except (BadRequestError, InternalError) as e:
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


@pytest.mark.parametrize("description, name_value, should_pass", updated_name_values)
def test_update_service_account_with_values(client, service_account, description, name_value, should_pass):
    responses = list()
    try:
        service_account_response = client.accounts.create(service_account, timeout=30)
        if service_account_response and service_account_response.account:
            responses.append(service_account_response)

        account = service_account_response.account
        account.name = name_value
        updated_service_account_response = client.accounts.update(account)
        assert name_value == updated_service_account_response.account.name
    except Exception as e:
        if should_pass and responses:
            e.msg = f"{e.msg}: {responses[-1].name}"
            raise e
    finally:
        for response in responses:
            response_id = response.account.id
            client.accounts.delete(id=response_id)


@pytest.mark.parametrize("suspend_value, suspend", suspend_values)
def test_suspend_service_account(client, service_account, suspend_value, suspend):
    responses = list()
    try:
        service_account_response = client.accounts.create(service_account, timeout=30)
        if service_account_response and service_account_response.account:
            responses.append(service_account_response)

        account = service_account_response.account
        account.suspended = suspend_value
        updated_service_account = client.accounts.update(account)

        # Filter for values and validate ID is in the list or not
        suspended_accounts = list(client.accounts.list("suspended:true"))
        updated_account = None
        for suspended in suspended_accounts:
            if account.id == suspended.id:
                updated_account = suspended

        if (updated_account and updated_account.suspended) and not suspend:
            raise AssertionError(f"Service Account was suspended when they should not have been.")
        elif updated_account is None and suspend:
            raise AssertionError(f"Service Account was not suspended when they should not have been.")
    finally:
        for response in responses:
            client.accounts.delete(response.account.id)


@pytest.mark.parametrize("description, delete_value, should_pass", delete_values)
def test_delete_service_account(client, service_account, description, delete_value, should_pass):
    service_account_response = None
    cleanup = True
    try:
        service_account_response = client.accounts.create(service_account, timeout=30)
        try:
            if delete_value == "REPLACE_ME":
                delete_value = service_account_response.account.id
                cleanup = False

            delete_response = client.accounts.delete(delete_value)
            assert delete_response and should_pass, "There should not have been a delete response"
        except (NotFoundError, Exception) as e:
            if should_pass:
                e.msg = f"{e.msg}: {delete_value}"
                raise e
    finally:
        if service_account_response and cleanup:
            client.accounts.delete(service_account_response.account.id)