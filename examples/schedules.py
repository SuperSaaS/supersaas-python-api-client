#!/usr/bin/env python3

import sys

from SuperSaaS import Client

print("# SuperSaaS Schedules Example")
client = Client.instance()

if not (client.account_name and client.api_key):
    print(
        "ERROR! Missing account credentials. Rerun the script with your credentials, e.g."
    )
    print(
        "    SSS_API_ACCOUNT_NAME=<myaccountname> SSS_API_KEY=<myapikey> python3 ./examples/schedules.py"
    )
    sys.exit(1)

client.verbose = True

print("listing schedules...")
print("#### client.schedules.list()")
schedules = client.schedules.list()

print("listing schedule resources...")
for i in range(min(10, len(schedules))):
    print(f"#### client.schedules.resources({schedules[i].id})")
    # Capacity schedules have no resources, the API returns an error for them
    try:
        client.schedules.resources(schedules[i].id)
    except Exception as e:
        print(
            f"Error fetching resources for schedule {schedules[i].id}: {e}"
        )

print("listing fields...")
for i in range(min(10, len(schedules))):
    print(f"#### client.schedules.field_list({schedules[i].id})")
    client.schedules.field_list(schedules[i].id)
