#!/usr/bin/python

import os
from datetime import datetime, timedelta
from SuperSaaS import Client

print("# SuperSaaS Slots Example")

if not (Client.instance().account_name and Client.instance().api_key):
    print(
        "ERROR! Missing account credentials. Rerun the script with your credentials, e.g."
    )
    print(
        "    SSS_API_ACCOUNT_NAME=<myaccountname> SSS_API_KEY=<myapikey> python3 ./examples/slots.py"
    )
    exit()

Client.instance().verbose = True

if not 'SSS_API_SCHEDULE' in os.environ:
    print(
        "ERROR! Missing schedule id (of a capacity type schedule). Rerun the script with your schedule id, e.g."
    )
    print("    SSS_API_SCHEDULE=<scheduleid> python3 ./examples/slots.py")
    exit()

schedule_id = os.environ['SSS_API_SCHEDULE']

print("listing slots...")
print(f"#### Client.instance().slots.list({schedule_id}, None, None, 25)")
slots = Client.instance().slots.list(schedule_id, None, None, 25)

if len(slots) > 0:
    slot_id = slots[0].id
    print("getting slot...")
    print(f"#### Client.instance().slots.get({schedule_id}, {slot_id})")
    Client.instance().slots.get(schedule_id, slot_id)

# Creating, updating and deleting slots changes your schedule data, so only run it when asked to
if os.environ.get('SSS_API_DESTRUCTIVE') == 'true':
    start_time = datetime.now() + timedelta(days=30)
    params = {
        'start': start_time,
        'finish': start_time + timedelta(hours=1),
        'title': 'Example slot',
        'capacity': 10
    }
    print("creating slot...")
    print(f"#### Client.instance().slots.create({schedule_id}, {params})")
    location = Client.instance().slots.create(schedule_id, params)['location']
    slot_id = location.rsplit('/', 1)[-1].split('.')[0]

    print("updating slot...")
    Client.instance().slots.update(schedule_id, slot_id, {'capacity': '-'})

    print("deleting slot...")
    Client.instance().slots.delete(schedule_id, slot_id)
else:
    print(
        "skipping create/update/delete (set SSS_API_DESTRUCTIVE=true to run them)..."
    )
