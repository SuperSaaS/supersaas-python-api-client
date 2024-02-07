#!/usr/bin/python

import os, re, random
from datetime import datetime, timedelta
from SuperSaaS import Client

print("# SuperSaaS Appointments Example")

if not (Client.instance().account_name and Client.instance().api_key):
    print(
        "ERROR! Missing account credentials. Rerun the script with your credentials, e.g."
    )
    print(
        "    SSS_API_ACCOUNT_NAME=<myaccountname> SSS_API_KEY=<myapikey> python3 ./examples/appointments.py"
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

user_id = None

# User is needed for some of these so either you have created one or this creates one for you
if 'SSS_API_USER' not in os.environ:
    params = {
        'full_name': 'Example',
        'name': 'example@example.com',
        'email': 'example@example.com',
    }

    user = Client.instance().users.create(params)
    match = re.search(r'users/(\d+)\.json', user.get('location', ''))
    if match:
        user_id = match.group(1)
        print(f"#New user created {user_id}")
    else:
        print("Failed to create user")

description = None
if user_id:
    description = '1234567890.'
    params = {
        'full_name': 'Example',
        'description': description,
        'name': 'example@example.com',
        'email': 'example@example.com',
        'mobile': '555-5555',
        'phone': '555-5555',
        'address': 'addr'
    }
    if 'SSS_API_SLOT' in os.environ:
        params['slot_id'] = os.environ.get('SSS_API_SLOT', None)
    else:
        days = random.randint(1, 30)
        start_time = datetime.now() + timedelta(days=days)
        params['start'] = start_time
        params['finish'] = start_time + timedelta(hours=1)

    print("creating new appointment...")
    print(
        f"#### SupersaasClient.instance().appointments.create({schedule_id}, {user_id}, {params})"
    )
    # Assuming SupersaasClient has a similar API in Python
    Client.instance().appointments.create(schedule_id, user_id, params)
else:
    print(
        "skipping create/update/delete (NO DESTRUCTIVE ACTIONS FOR SCHEDULE DATA)..."
    )

if 'SSS_API_USER' in os.environ:
    user_id = os.environ['SSS_API_USER']
    print("listing agenda...")
    if 'SSS_SLOT' in os.environ:
        print(
            "#### Client.instance.appointments.agenda_slots({}, '{}')".format(
                schedule_id, user_id))
        changes = Client.instance().appointments.agenda_slots(
            schedule_id, user_id)
    else:
        print("#### Client.instance.appointments.agenda({}, '{}')".format(
            schedule_id, user_id))
        changes = Client.instance().appointments.agenda(schedule_id, user_id)

print("listing appointments...")
print("#### Client.instance().appointments.list({}, nil, nil, 25)".format(
    schedule_id))

appointments = Client.instance().appointments.list(schedule_id, None, None, 25)

# Check if there are appointments and get a random one
if len(appointments) > 0:
    appointment_id = random.choice(appointments).id
    print("getting appointment...")
    print(f"#### Client.instance().appointments.get({appointment_id})")
    Client.instance().appointments.get(schedule_id, appointment_id)

print("listing changes...")
from_time = datetime.now() - timedelta(days=120)

print("listing changes...")
if 'SSS_SLOT' in os.environ:
    print(
        "Legacy call, you can achieve the same by using changes with the slot variable as True, see docs"
    )
    print(
        f"#### Client.instance.appointments.changes_slots({schedule_id}, '{datetime.now()}')"
         )
    Client.instance().appointments.changes_slots(schedule_id, datetime.now())
    print(
        "Instead of the above you can use changes ike this to achieve the same"
    )
    changes = Client.instance().appointments.changes(schedule_id, from_time,
                                                     None, True)
else:
    print(
        f"#### Client.instance().appointments.changes({schedule_id}, '{from_time}', '{None}', {True or 'false'})"
    )
    Client.instance().appointments.changes(schedule_id, from_time, None,
                                           False)

print("listing available...")
from_time = datetime.now()
print(
    f"#### Client.instance().appointments.available({schedule_id}, '{from_time}')"
)
Client.instance().appointments.available(schedule_id, from_time)

print("Appointments for a single user...")
users = Client.instance().users.list(None, 1)
if users:
    user = users[0]
    print(
        f"#### Client.instance().appointments.agenda({schedule_id}, {user.id}, '{from_time}')"
    )
    Client.instance().appointments.agenda(schedule_id, user.id, from_time)

# Update and delete appointments, this part is commented out as it is quite destructive
# for appointment in appointments:
#     print(f"{description} == {appointment.description}")
#     if description == appointment.description:
#         print("updating appointment...")
#         print(f"#### Client.instance().appointments.update({schedule_id}, {appointment.id}, {{...}})")
#         Client.instance().appointments.update(schedule_id, appointment.id, {'country': 'FR', 'address': 'Rue 1'})
#
#     print("deleting appointment...")
#     print(f"#### Client.instance().appointments.delete({schedule_id}, {appointment.id})")
#     Client.instance().appointments.delete(schedule_id, appointment.id)
#     break

if user_id:
    print("Get agenda for a single user")
    agenda = Client.instance().appointments.agenda(schedule_id, user_id)

print(
    "Get available slots or bookings, you can also for availability from the future with from_time, length of booking and add a resource if required"
)
bookings = Client.instance().appointments.available(schedule_id)

print(
    "This API allows you to retrieve all appointments or slots from a schedule within a time range. There are plenty of paramters to help you narrow down your search, please refer to the docs for more information"
)
range = Client.instance().appointments.range(schedule_id)

# Delete user based on environment variable condition
if not os.environ.get('SSS_API_USER'):
    Client.instance().users.delete(user_id)
