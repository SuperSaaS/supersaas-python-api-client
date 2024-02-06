#!/usr/bin/env python

from SuperSaaS import Client

print("# SuperSaaS Promotions Example")

client = Client.instance()  # Adjust based on your actual client instantiation method

# Check for environment variables for account credentials
if not (client.account_name and client.api_key):
    print("ERROR! Missing account credentials. Rerun the script with your credentials, e.g.,")
    print("SSS_API_ACCOUNT_NAME=<myaccountname> SSS_API_KEY=<xxxxxxxxxxxxxxxxxxxxxx> python examples/users.py")
    exit()

print(f"## Account:  {client.account_name}")
print(f"## API KEY: {'*' * len(client.api_key)}")

client.verbose = True

print("listing promotions...")
print("#### client.promotions.list")
promotions = client.promotions.list()

for i in range(min(10, len(promotions))):
    print("A promotion")
    print(f"#### client.promotion({promotions[i].id})")
    client.promotions.promotion(promotions[i].code)

# Uncomment to try out duplicating a promotional code
# import secrets
# print("duplicate promotional code")
# new_code = f"pcode{secrets.token_hex(4)}"
# print(f"#### client.promotions.duplicate_promotion_code('{new_code}', '{promotions[0].code}')")
# client.promotions.duplicate_promotion_code(new_code, promotions[0].code)
