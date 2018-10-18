#!/usr/bin/python

import os
from datetime import datetime
from SuperSaaS import Client

print("\n\r# SuperSaaS Appointments Example\n\r")

if not (Client.instance().account_name and Client.instance().password):
    print("ERROR! Missing account credentials. Rerun the script with your credentials, e.g.\n\r")
    print("    SSS_API_ACCOUNT_NAME=<myaccountname> SSS_API_PASSWORD=<mypassword> ./examples/schedules.py\n\r")
    exit()

Client.instance().verbose = True

if not 'SSS_API_SCHEDULE' in os.environ:
    print("ERROR! Missing schedule id. Rerun the script with your schedule id, e.g.\n\r")
    print("    SSS_API_SCHEDULE=<scheduleid> ./examples/appointments.py\n\r")
    exit()

schedule_id = os.environ['SSS_API_SCHEDULE']

print("\n\rlisting appointments...")
print("\n\r#### Client.instance().appointments.list({}, nil, nil, 25)\n\r".format(schedule_id))

schedules = Client.instance().appointments.list(schedule_id, True, datetime.now(), 10)