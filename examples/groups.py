#!/usr/bin/env python3

import sys

from SuperSaaS import Client

print("# SuperSaaS Groups Example")
client = Client.instance()

if not (client.account_name and client.api_key):
    print(
        "ERROR! Missing account credentials. Rerun the script with your credentials, e.g."
    )
    print(
        "    SSS_API_ACCOUNT_NAME=<myaccountname> SSS_API_KEY=<myapikey> python3 ./examples/groups.py"
    )
    sys.exit(1)

print(f"## Account:  {client.account_name}")
print(f"## API KEY: {'*' * len(client.api_key)}")

client.verbose = True

print("listing groups...")
print("#### client.groups.list()")
client.groups.list()
