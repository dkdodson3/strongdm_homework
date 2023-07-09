import pytest
from strongdm import BadRequestError, AccountAttachment

from tests.conftest import punctuation_list, accepted_punctuation_failures


# def test_delete_roles(client):
#     roles = list(client.roles.list('name:ROLL_*'))
#     for role in roles:
#         client.roles.delete(role.id)


def test_add_role(client, role):
    role_response = None
    try:
        role.name = "If I were a rich man..."
        role_response = client.roles.create(role, timeout=30)
    finally:
        if role_response:
            client.roles.delete(role_response.role.id)


@pytest.mark.parametrize("punc", punctuation_list)
def test_add_role_with_punctuation(client, role, punc):
    role_response = None
    role.name = f"{role.name}{punc}"
    try:
        role_response = client.roles.create(role, timeout=30)
    except (BadRequestError, Exception) as e:
        if punc not in accepted_punctuation_failures:
            e.msg = f"{e.msg}: role.name is '{role.name}'"
            raise e
    finally:
        if role_response:
            client.roles.delete(role_response.role.id)


def test_update_role(client, role):
    role_response = None
    try:
        role_response = client.roles.create(role, timeout=30)
        update_role = role_response.role
        update_role.name = "If I were a rich man..."
        current_role = client.roles.update(update_role)

        assert role.name != current_role.role.name, \
            f"The role name did not get updated to '{update_role.name}', but was '{current_role.role.name}'"

    finally:
        if role_response:
            client.roles.delete(role_response.role.id)


def test_delete_role(client, role):
    role_response = None
    should_delete = True
    try:
        role_response = client.roles.create(role, timeout=30)

        created_role = role_response.role
        deleted_response = client.roles.delete(created_role.id)
        if deleted_response:
            should_delete = False

        roles = client.roles.list('managed:false')

        for item in roles:
            assert item.id != created_role.id, f"Role '{created_role.id}' was not deleted as expected."
    finally:
        if role_response and should_delete:
            client.roles.delete(role_response.role.id)


def test_role_grant_by_tag(client, role, user, resource_postgres):
    user.tags = {"name": "foo"}
    resource_postgres.tags = {"name": "foo"}
    user_response = client.accounts.create(user, timeout=30)
    resource_postgres_response = client.resources.create(resource_postgres)
    role_response = client.roles.create(role, timeout=30)
    try:
        current_role = role_response.role
        current_role.access_rules = [
            {
                "tags": {"name": "foo"},
            },
        ]
        current_role = client.roles.update(current_role)
        account_attachment = AccountAttachment(
            account_id=user_response.account.id,
            role_id=current_role.role.id
        )

        account_attachment_response = client.account_attachments.create(account_attachment, timeout=30)
        account_attachments = list(client.account_attachments.list(f'account_id:{user_response.account.id}'))

        assert account_attachments[0].role_id == current_role.role.id, "Attachment was not made for the correct role"
    finally:
        client.accounts.delete(user_response.account.id)
        client.resources.delete(resource_postgres_response.resource.id)
        client.roles.delete(role_response.role.id)