
import pytest
from strongdm import BadRequestError, InternalError, NotFoundError

from tests.conftest import name_values, punctuation_list, accepted_punctuation_failures, unicode_whitespace_characters, \
    email_values, updated_name_values, updated_email_values, suspend_values, delete_values


# def test_delete_users(client):
#     """
#     Quickly delete users
#     """
#     users = list(client.accounts.list('permission_level:user'))
#     for user in users:
#         client.accounts.delete(user.id)


@pytest.mark.parametrize("punc", punctuation_list)
def test_add_user_with_punctuation(client, user, punc):
    """
    A parameterized test to verify users can have specific punctuation
    """
    user_response = None
    user.first_name = f"{user.first_name}{punc}"
    try:
        user_response = client.accounts.create(user, timeout=30)
    except BadRequestError as e:
        if punc not in accepted_punctuation_failures:
            e.msg = f"{e.msg}: {user.first_name}"
            raise e
    finally:
        if user_response:
            client.accounts.delete(user_response.account.id)


@pytest.mark.parametrize("description, name_value, should_pass", name_values)
def test_add_user_with_different_values(client, user, description, name_value, should_pass):
    """
    A parameterized test to add service accounts with different names
    """
    user_response = None
    user.first_name = name_value
    try:
        user_response = client.accounts.create(user, timeout=30)
    except (BadRequestError, InternalError) as e:
        if should_pass:
            e.msg = f"{e.msg}: {user.first_name}"
            raise e
    finally:
        if user_response:
            client.accounts.delete(user_response.account.id)


@pytest.mark.parametrize("description, unicode_value", unicode_whitespace_characters)
def test_add_user_with_unicode_values(client, user, description, unicode_value):
    """
    A parameterized test to add users with unicode values in the name
    """
    user_response = None
    user.first_name = f"a_{unicode_value}{user.first_name}"
    try:
        user_response = client.accounts.create(user, timeout=30)
    except (BadRequestError, InternalError) as e:
        e.msg = f"{e.msg}: {user.first_name}"
        raise e
    finally:
        if user_response:
            client.accounts.delete(user_response.account.id)


@pytest.mark.parametrize("description, email_value, should_pass", email_values)
def test_add_user_with_different_emails(client, user, description, email_value, should_pass):
    """
    A parameterized test to verify adding users with different email values
    """
    user_response = None
    try:
        user.email = email_value
        user_response = client.accounts.create(user, timeout=30)
        assert bool(user) == should_pass, f"Email of '{user.email}' should not have been allowed to be created"
    except (BadRequestError, InternalError, TypeError) as e:
        if should_pass:
            e.msg = f"{e.msg}: {user.email}"
            raise e
    finally:
        if user_response:
            client.accounts.delete(user_response.account.id)


def test_add_user_with_same_email(client, user):
    """
    A test to verify that a user cannot be adde with the same email address
    :param client:
    :param user:
    :return:
    """
    user_response = None
    try:
        user_response = client.accounts.create(user, timeout=30)
        client.accounts.create(user, timeout=30)
        raise Exception(f"User with the same email of '{user.email}' should not be allowed to be created")
    finally:
        if user_response:
            client.accounts.delete(user_response.account.id)


@pytest.mark.parametrize("description, name_value, should_pass", updated_name_values)
def test_update_user_with_name_values(client, user, description, name_value, should_pass):
    """
    A parameterized test to add users with different names
    """
    responses = list()
    try:
        user_response = client.accounts.create(user, timeout=30)
        if user_response and user_response.account:
            responses.append(user_response)

        account = user_response.account
        account.first_name = name_value
        updated_user_response = client.accounts.update(account)
        assert name_value == updated_user_response.account.first_name
    except Exception as e:
        if should_pass and responses:
            e.msg = f"{e.msg}: {responses[-1].first_name}"
            raise e
    finally:
        for response in responses:
            response_id = response.account.id
            client.accounts.delete(id=response_id)


@pytest.mark.parametrize("description, email_value, should_pass", updated_email_values)
def test_update_user_with_different_emails(client, user, description, email_value, should_pass):
    """
    A parameterized test to verify updating users with different email values
    """
    responses = list()
    try:
        user_response = client.accounts.create(user, timeout=30)
        if user_response and user_response.account:
            responses.append(user_response)

        account = user_response.account
        account.email = email_value
        updated_user = client.accounts.update(account)

        assert bool(updated_user) == should_pass, f"Email of '{updated_user.email}' should not have been allowed to update"
    except (BadRequestError, InternalError, TypeError) as e:
        if should_pass:
            e.msg = f"{e.msg}: {email_value}"
            raise e
    finally:
        for response in responses:
            client.accounts.delete(response.account.id)


@pytest.mark.parametrize("suspend_value, suspend", suspend_values)
def test_suspend_user(client, user, suspend_value, suspend):
    """
    A parameterized test to verify the suspending of users
    """
    responses = list()
    try:
        user_response = client.accounts.create(user, timeout=30)
        if user_response and user_response.account:
            responses.append(user_response)

        account = user_response.account
        account.suspended = suspend_value
        client.accounts.update(account)

        # Filter for values and validate ID is in the list or not
        suspended_accounts = list(client.accounts.list("suspended:true"))
        updated_account = None
        for suspended in suspended_accounts:
            if account.id == suspended.id:
                updated_account = suspended

        if (updated_account and updated_account.suspended) and not suspend:
            raise AssertionError(f"User was suspended when they should not have been.")
        elif updated_account is None and suspend:
            raise AssertionError(f"User was not suspended when they should not have been.")
    finally:
        for response in responses:
            client.accounts.delete(response.account.id)


@pytest.mark.parametrize("description, delete_value, should_pass", delete_values)
def test_delete_user(client, user, description, delete_value, should_pass):
    """
    A parameterized test to verify the deletion of users
    """
    user_response = None
    cleanup = True
    try:
        user_response = client.accounts.create(user, timeout=30)
        try:
            if delete_value == "REPLACE_ME":
                delete_value = user_response.account.id
                cleanup = False

            delete_response = client.accounts.delete(delete_value)
            assert delete_response and should_pass, "There should not have been a delete response"
        except (NotFoundError, Exception) as e:
            if should_pass:
                e.msg = f"{e.msg}: {delete_value}"
                raise e
    finally:
        if user_response and cleanup:
            client.accounts.delete(user_response.account.id)
