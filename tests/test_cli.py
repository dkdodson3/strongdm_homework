"""
--- CLI Tests ---
Filter Role
Delete Role

Filter Resource
Remove Resource
"""
import json
import os

import pexpect

from tests.conftest import get_user


def test_add_find_delete_user():
    fileloc = "./add_user.json"
    user = get_user()
    with open(fileloc, "w") as user_file:
        json_template = [
            {
                "firstName": user.first_name,
                "lastName": user.last_name,
                "email": user.email,
                "tags": ""
            }
        ]
        user_file.write(json.dumps(json_template, indent=4))
    try:
        pexpect.run(f'sdm admin users add --file {fileloc}')
        output = pexpect.run(f'sdm admin users list --json --filter "first_name:{user.first_name}')
        user_list = json.loads(output.decode("utf-8"))
        assert user_list[0]["lastName"] == user.last_name, "Filter returned the wrong user"

        pexpect.run(f'sdm admin users delete {user.email}')
        output2 = pexpect.run(f'sdm admin users list --json --filter "first_name:{user.first_name}')
        user_list2 = json.loads(output2.decode("utf-8"))
        assert len(user_list2) == 0, "Deletion of user did not happen"
    finally:
        os.remove(fileloc)
