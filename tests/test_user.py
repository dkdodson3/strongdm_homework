

"""
# https://www.stickyminds.com/article/how-skeleton-strings-can-help-your-testing
Update User - Name - Name Change
Update User - Name - [space]
Update User - Email - Email Change
Update User - Email - Invalid Email
Update User - Email - null
Update User - Remote Identity - No Name
Update User - Remote Identity - [space]
Update User - Remote Identity - flibberty gibbet
Update User - Remote Identity - Different Punctuations (`~!@#$%^&*()_+|}{[]\":;'<>?/.,’)
Update User - Remote Identity - Foreign Characters (Ľuboš Bartečko)
Update User - Remote Identity - Chinese Characters (您可以撼動它)
Update User - ???'managed:false'???

Create ServiceAccount - No Name
Create ServiceAccount - [space]
Create ServiceAccount - foo bar
Create ServiceAccount - Email address instead of name
Create ServiceAccount - [MIN Characters]
Create ServiceAccount - [MAX Characters]
X Create ServiceAccount - Different Punctuations (`~!@#$%^&*()_+|}{[]\":;'<>?/.,’)
Create ServiceAccount - Foreign Characters (Ľuboš Bartečko)
Create ServiceAccount - Chinese Characters (您可以撼動它)
Create ServiceAccount - HTML (<a href=”http://cnn.com”>CNN</a>)
Create ServiceAccount - Javascript (javascript:alert("Danger!");)
Create ServiceAccount - SQL Injection (drop table Users;)

Update ServiceAccount - Name - Name Change
Update ServiceAccount - Remote Identity - No Name
Update ServiceAccount - Remote Identity - [space]
Update ServiceAccount - Remote Identity - flibberty gibbet
Update ServiceAccount - Remote Identity - Different Punctuations (`~!@#$%^&*()_+|}{[]\":;'<>?/.,’)
Update ServiceAccount - Remote Identity - Foreign Characters (Ľuboš Bartečko)
Update ServiceAccount - Remote Identity - Chinese Characters (您可以撼動它)

Suspend User - True
Suspend User - False
Suspend User - "true"
Suspend User - 0
Suspend User - 1

Suspend ServiceAccount - True
Suspend ServiceAccount - False
Suspend ServiceAccount - "true"
Suspend ServiceAccount - 0
Suspend ServiceAccount - 1

Delete User - Good int
Delete User - Bad int
Delete User - String int
Delete User - String Bob
Delete User - [space]
Delete User - null

Delete ServiceAccount - Good int
Delete ServiceAccount - Bad int
Delete ServiceAccount - String int
Delete ServiceAccount - String Bob
Delete ServiceAccount - [space]
Delete ServiceAccount - null


--- ROLES ---
Suspend Role
Create Role
Delete Role
Update Role
- Id
    + Valid
    + Invalid
- Name
- Access Rules
    + Static and Dynamic
    + Static - One
    + Static - Multi

        {
          "id": "r-6b73c71964a8920e",
          "name": "asdf",
          "accessRules": [
            {
              "ids": ["r-6b73c71964a8920f", "r-6b73c71964a8920g"],
              "dbType": null,
              "tags": [],
              "naturalPolicy": ""
            }
          ]
        }
    + Dynamic - One
    + Dynamic - Multi
        {
          "id": "r-6b73c71964a8920e",
          "name": "asdf",
          "accessRules": [
            {
              "ids": [],
              "dbType": "kubernetes", # dbtype = Any="", DataSource, Website, Cluster, Server, Cloud
              "tags": [
                {
                  "name": "wordwasp",
                  "value": ""
                }
              ],
              "naturalPolicy": ""
            }
          ]
        }

Assign Roles to user
Assign Roles to tags
Remove Roles from user
Remove Roles from tags
Grant Roles all datasources
Revoke Roles from all datasources
List Roles - Filter (name, tags, managed, id)

--- RESOURCES ---
Add Resource - DB
Add Resource - Linux Server - SSH Server
Add Resource - K8
Add Resource - Gateway
Add Resource - Relay
List Resources - Filter - "healthy:true", "healthy:false",
List Resources - Filter - DB Specific
List Resources - Filter - Linux Server Specific
List Nodes - Filter - Gatewqy, Relay




"""
import pytest
import strongdm
from strongdm import BadRequestError, InternalError, AlreadyExistsError

from tests.conftest import name_values, punctuation_list, accepted_punctuation_failures, unicode_whitespace_characters, \
    email_values

"""
./sdm admin
   clouds                                  manage clouds
   clusters                                manage clusters
   kubernetes, k8s                         manage Kubernetes cluster
   ports                                   manage port overrides
   rdp                                     manage RDP servers
   relays, relay                           manage relays
   remote-identities, remote-identity, ri  manage remote identities
   resources                               manage resources
   rest                                    make custom HTTP REST requests
   roles                                   manage roles
   secretstores, secretstore               manage secret stores
   servers                                 manage servers
   services, svc, service                  manage service accounts
   ssh                                     manage SSH public key servers
   users                                   manage users
   websites, web, http                     manage websites

"""


"""
--- Bugs ---
./sdm admin ri list  # this is not showing anything
Unicode Character Spaces are allowed but not a normal space
Can add invalid email addresses
"""


def test_healthy_resources(client, user):
    # https://www.strongdm.com/docs/cli/filters/

    # healthy_resources = list(client.resources.list('healthy:true'))
    # unhealthy_resources = list(client.resources.list('healthy:false'))
    # ri_resources = list(client.resources.list('remoteidentityenabled:true'))

    # relays = list(client.nodes.list('type:relay'))

    user.first_name = None
    user.last_name = "1"
    response = client.accounts.create(user, timeout=30)

    pass


@pytest.mark.parametrize("punc", punctuation_list)
def test_add_user_with_punctuation(client, user, punc):
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
    user_response = None
    user.first_name = name_value
    try:
        user_response = client.accounts.create(user, timeout=30)
    except Exception as e:  # BadRequestError, InternalError
        if should_pass:
            e.msg = f"{e.msg}: {user.first_name}"
            raise e
    finally:
        if user_response:
            client.accounts.delete(user_response.account.id)


# REALLY NOT SURE IF THESE SHOULD BE PASSING....
@pytest.mark.parametrize("description, unicode_value", unicode_whitespace_characters)
def test_add_user_with_unicode_values(client, user, description, unicode_value):
    user_response = None
    user.first_name = f"a_{unicode_value}{user.first_name}"
    try:
        user_response = client.accounts.create(user, timeout=30)
    except Exception as e:  # BadRequestError, InternalError
        e.msg = f"{e.msg}: {user.first_name}"
        raise e
    finally:
        if user_response:
            client.accounts.delete(user_response.account.id)


@pytest.mark.parametrize("description, email_value, should_pass", email_values)
def test_add_user_with_different_emails(client, user, description, email_value, should_pass):
    user_response = None
    user.email = email_value
    try:
        user_response = client.accounts.create(user, timeout=30)
        if not should_pass:
            raise Exception(f"Email of '{user.email}' should not have been allowed")
    except BadRequestError as e:  # BadRequestError, InternalError, TypeError
        if should_pass:
            e.msg = f"{e.msg}: {user.email}"
            raise e
    finally:
        if user_response:
            client.accounts.delete(user_response.account.id)


def test_add_user_with_same_email(client, user):
    user_response = None
    try:
        user_response = client.accounts.create(user, timeout=30)
        user_response2 = client.accounts.create(user, timeout=30)
        raise Exception(f"User with the same email of '{user.email}' should not be allowed to be created")
    except AlreadyExistsError as e:
        pass
    finally:
        if user_response:
            client.accounts.delete(user_response.account.id)