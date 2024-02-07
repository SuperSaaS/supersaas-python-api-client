#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from SuperSaaS import Client  # Adjust based on actual Python package or module

print("# SuperSaaS Users Example")

client = Client.instance()

# Check for environment variables for account credentials
if not (client.account_name and client.api_key):
    print(
        "ERROR! Missing account credentials. Rerun the script with your credentials, e.g.,"
    )
    print(
        "SSS_API_ACCOUNT_NAME=<myaccountname> SSS_API_KEY=<xxxxxxxxxxxxxxxxxxxxxx> python examples/users.py"
    )
    exit()

print(f"## Account:  {client.account_name}")
print(f"## API Key: {'*' * len(client.api_key)}")

client.verbose = True

print('creating new user...')
print("#### client.users.create({...})")
params = {
    'full_name': 'Example',
    'name': 'example@example.com',
    'email': 'example@example.com'
}
client.users.create(params)
new_user_id = None

print("listing users...")
print("#### client.users.list(None, 50)")

users = client.users.list(None, 50)
for user in users:
    if user.name == params['email']:
        new_user_id = user.id

if new_user_id:
    print("getting user...")
    print(f"#### client.users.get({new_user_id})")
    user = client.users.get(new_user_id)

    print("updating user...")
    print(f"#### client.users.update({new_user_id})")
    client.users.update(new_user_id, {'country': 'FR', 'address': 'Rue 1'})

    print("deleting user...")
    print(f"#### client.users.delete({user.id})")
    client.users.delete(user.id)
else:
    print("... did not find user in list")

print("creating user with errors...")
print("#### client.users.create")
try:
    client.users.create({'name': 'error'})
except Exception as e:  # Adjust based on actual exception handling in your Python client
    print(f"This raises an error {str(e)}")

print("#### client.users.field_list")
client.users.field_list()
