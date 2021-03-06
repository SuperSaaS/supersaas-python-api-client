#!/usr/bin/python
from SuperSaaS import Client

print("\n\r# SuperSaaS Schedules Example\n\r")

if not (Client.instance().account_name and Client.instance().api_key):
    print("ERROR! Missing account credentials. Rerun the script with your credentials, e.g.\n\r")
    print("    SSS_API_ACCOUNT_NAME=<myaccountname> passwSSS_API_KEY=<myapikey> ./examples/schedules.py\n\r")

Client.instance().verbose = True

print("\n\rlisting schedules...")
print("\n\r#### Client.instance().schedules.list()\n\r")
schedules = Client.instance().schedules.list()
