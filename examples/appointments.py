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

if 'SSS_API_USER' in os.environ:
    user_id = os.environ['SSS_API_USER']
    print("\n\rlisting agenda...")
    if 'SSS_SLOT' in os.environ:
        print("\n\r#### Client.instance.appointments.agenda_slots({}, '{}')\n\r".format(schedule_id, user_id))
        changes = Client.instance().appointments.agenda_slots(schedule_id, user_id)
    else:
        print("\n\r#### Client.instance.appointments.agenda({}, '{}')\n\r".format(schedule_id, user_id))
        changes = Client.instance().appointments.agenda(schedule_id, user_id)

print("\n\rlisting changes...")
if 'SSS_SLOT' in os.environ:
    print("\n\r#### Client.instance.appointments.changes_slots({}, '{}')\n\r".format(schedule_id, datetime.now()))
    changes = Client.instance().appointments.changes_slots(schedule_id, datetime.now())
else:
    print("\n\r#### Client.instance.appointments.changes({}, '{}')\n\r".format(schedule_id, datetime.now()))
    changes = Client.instance().appointments.changes(schedule_id, datetime.now())

