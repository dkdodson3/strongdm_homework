"""
--- Bugs ---
./sdm admin ri list  # this is not showing anything
Unicode Character Spaces are allowed but not a normal spaces,
Improper handling of string for ("Over Max characters for Name", "a" * 1025, True)
    #   strongdm.errors.InternalError: cannot create service account: cannot create entry for service account storage: internal error: database error
Cli gives you a datasource template but does not allow you to use it...
It does not look like we are checking for a valid email address when creating or updating users except for an empty entry
"""

"""
Improve Tests:
Make sure I am deleting and populating the correct items at the beginning of the test rather than at the end.
Some of the tests should be only asserting/verifying one action but they are doing many
Add more real resources
Add more thought into relay and gateway access testing
This is not the best way to assert granting access worked I am just not sure how to find that with the api
Add more tests...
"""