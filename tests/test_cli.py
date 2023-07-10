import json

import pexpect
import tempfile

import pytest

from tests.conftest import get_user, get_role, get_resource_postgres


@pytest.fixture(name="tmp_file")
def tmp_file_fixture() -> tempfile.NamedTemporaryFile:
    """
    Quick way to generate and cleanup a tempfile
    :return: tempfile.NamedTemporaryFile
    """
    temporary_file = tempfile.NamedTemporaryFile(mode="w+")
    yield temporary_file
    temporary_file.close()


def test_add_find_delete_user(tmp_file):
    """
    Test that adds, finds, and deletes a user using the SDM cli
    """
    user_list = None
    delete_user = True

    # Creating an ADD template file
    user = get_user()
    json_template = [
        {
            "firstName": user.first_name,
            "lastName": user.last_name,
            "email": user.email,
            "tags": ""
        }
    ]
    tmp_file.write(json.dumps(json_template, indent=4))
    tmp_file.flush()

    try:
        # Adding a User
        pexpect.run(f'sdm admin users add --file {tmp_file.name}')

        # Finding and Verifying the user exists
        output = pexpect.run(f'sdm admin users list --json --filter "first_name:{user.first_name}')
        user_list = json.loads(output.decode("utf-8"))
        assert user_list and user_list[0]["lastName"] == user.last_name, "Filter returned the wrong user"

        # Deleting the user and Verifying that it was deleted
        pexpect.run(f'sdm admin users delete {user.email}')
        output2 = pexpect.run(f'sdm admin users list --json --filter "first_name:{user.first_name}')
        user_list2 = json.loads(output2.decode("utf-8"))
        assert len(user_list2) == 0, "Deletion of user did not happen"
        delete_user = False
    finally:
        if user_list and delete_user:
            pexpect.run(f'sdm admin users delete {user.email}')


def test_add_find_delete_role(tmp_file):
    role_list = None
    delete_role = True

    # Creating an ADD template file
    role = get_role()
    json_template = [
        {
            "name": role.name,
            "composite": False,
            "tags": ""
        }
    ]
    tmp_file.write(json.dumps(json_template, indent=4))
    tmp_file.flush()

    try:
        # Adding a Role
        pexpect.run(f'sdm admin roles add --file {tmp_file.name}')

        # Finding and Verifying the role exists
        output = pexpect.run(f'sdm admin roles list --json --filter "name:{role.name}')
        role_list = json.loads(output.decode("utf-8"))
        assert role_list and role_list[0]["name"] == role.name, "Filter returned the wrong role"

        # Deleting the role and Verifying that it was deleted
        pexpect.run(f'sdm admin roles delete {role_list[0]["id"]}')
        output2 = pexpect.run(f'sdm admin roles list --json --filter "name:{role.name}')
        role_list2 = json.loads(output2.decode("utf-8"))
        assert len(role_list2) == 0, "Deletion of role did not happen"
        delete_role = False
    finally:
        if role_list and delete_role:
            pexpect.run(f'sdm admin roles delete {role_list[0]["id"]}')


def test_add_find_delete_datasource(tmp_file):
    datasource_list = None
    delete_datasource = True

    # Creating an ADD template file
    datasource = get_resource_postgres()

    json_template = [
        {
            "bindInterface": "127.0.0.1",
            "database": datasource.database,
            "hostname": datasource.hostname,
            "name": datasource.name,
            "overrideDatabase": "true",
            "password": datasource.password,
            "port": datasource.port,
            "portOverride": "",
            "subdomain": "",
            "type": "postgres",
            "username": datasource.username
        }
    ]
    tmp_file.write(json.dumps(json_template, indent=4))
    tmp_file.flush()

    try:
        # Adding a postgres datasource
        pexpect.run(f'sdm admin datasources add postgres --file {tmp_file.name}')

        # Finding and Verifying the datasource exists
        output = pexpect.run(f'sdm admin datasources list --json --filter \'name:"{datasource.name}"\'')
        datasource_list = json.loads(output.decode("utf-8"))
        assert datasource_list and datasource_list[0]["name"] == datasource.name, "Filter returned the wrong datasource"

        # Deleting the datasource and Verifying that it was deleted
        pexpect.run(f'sdm admin datasources delete {datasource_list[0]["id"]}')
        output2 = pexpect.run(f'sdm admin datasources list --json --filter "name:{datasource.name}')
        role_list2 = json.loads(output2.decode("utf-8"))
        assert len(role_list2) == 0, "Deletion of datasource did not happen"
        delete_datasource = False
    finally:
        if datasource_list and delete_datasource:
            pexpect.run(f'sdm admin datasource delete {datasource_list[0]["id"]}')
