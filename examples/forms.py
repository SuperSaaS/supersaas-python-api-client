#!/usr/bin/python

import os
from SuperSaaS import Client

print("# SuperSaaS Forms Example")

if not (Client.instance().account_name and Client.instance().api_key):
    print(
        "ERROR! Missing account credentials. Rerun the script with your credentials, e.g."
    )
    print(
        "    SSS_API_ACCOUNT_NAME=<myaccountname> SSS_API_KEY=<myapikey> ./examples/forms.py"
    )
    exit()

Client.instance().verbose = True

if not 'SSS_API_SCHEDULE' in os.environ:
    print(
        "ERROR! Missing schedule id. Rerun the script with your schedule id, e.g."
    )
    print("    SSS_API_SCHEDULE=<scheduleid> ./examples/appointments.py")
    exit()

schedule_id = os.environ['SSS_API_SCHEDULE']

print(
    "You will need to create a form, and also attach the form to a booking, see documentation on how to do that"
)
print(
    "The below example will take a form in random, and if it is not attached to something then 404 error will be raised"
)

print("listing forms...")
print("#### Client.instance().forms.forms")

template_forms = Client.instance().forms.forms()

if template_forms:
    from random import choice
    template_form_id = choice(template_forms).id

    print("listing forms from account")
    print("#### Client.instance().forms.list")
    form_id = choice(
        Client.instance().instance().forms.list(template_form_id)).id

    print("getting form...")
    print(f"#### Client.instance().forms.get({form_id})")
    Client.instance().forms.get(form_id)
