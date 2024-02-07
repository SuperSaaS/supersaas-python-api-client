# SuperSaaS Python SDK

Online bookings/appointments/calendars in Python using the SuperSaaS scheduling platform - https://supersaas.com

The SuperSaaS API provides services that can be used to add online booking and scheduling functionality to an existing website or CRM software.

## Prerequisites

1. [Register for a (free) SuperSaaS account](https://www.supersaas.com/accounts/new), and
2. get your account name and API key on the [Account Info](https://www.supersaas.com/accounts/edit) page. 

##### Dependencies

Python 3.*

No external libraries. The supporting `urllib`/`urllib2` and `json`/`simplejson` standard libs are loaded conditionally.

## Installation

The SDK is available from PyPi and can be installed using pip, e.g.

    $ pip install supersaas-api-client

## Configuration

The SuperSaaS client can be created in two ways:

1. Simply initialize a `Client()` instance
2. Obtain the singleton instnace by calling the helper method

### Creating a normal instance
Simply create a new client instance manually:
    
```python
from SuperSaaS import Client, Configuration

# Initialize client with authorization credentials
config = Configuration()

client = Client(config)
client.account_name = 'your_account_name'
client.api_key = 'your_api_key'

# Do API calls
client.schedules.list()
...
```

### Get(or create) the singleton instance
Use the helper method `Client.instance()` to deal with the **singleton** instance:

```python
from SuperSaaS import Client

# Initialize the singleton with authorization credentials
Client.instance().configure(
    account_name = 'your_account_name',
    api_key = 'your_api_key'
)    

# Do API calls
Client.instance().schedules.list()
...
```

### Configuring the client
    
> Note, ensure that `configure` is called before `instance`, otherwise the client will be initialized with configuration defaults.

If the client isn't configured explicitly, it will use default `ENV` variables for the account name and api key.

    ENV['SSS_API_ACCOUNT_NAME'] = 'your-env-supersaas-account-name'
    ENV['SSS_API_KEY'] = 'your-env-supersaas-api-key' 
    Client.instance().account_name #=> 'your-env-supersaas-account-name'
    Client.instance().api_key #=> 'your-env-supersaas-api-key'
    
All configuration options can be individually set on the client.

    Client.instance().api_key = 'xxxxxxxxxxxxxxxxxxxxxx' 
    Client.instance().verbose = True
    ...

Avaiable configuration options are:
| Attribute | Default value | Descriptions |  |  |
|----------------|----------------------------|-------------------------------------------------------------------------------------|---|---|
| account_name | '' | Your account name |  |  |
| api_key | '' | Your api key |  |  |
| verbose | False | Whether to print the HTTP request/response data to console. For debugging purpose.  |  |  |
| host | Configuration.DEFAULT_HOST | Server host. Normally you won't need to specify this. |  |  |

For implementaion detail check the `Configuration()` class in  [SuperSaas/Client.py](SuperSaaS/Client.py)

## API Methods

Details of the data structures, parameters, and values can be found on the developer documentation site:

https://www.supersaas.com/info/dev

#### List Schedules

Get all account schedules:

    Client.instance().schedules.list()
    
#### List Resource

Get all services/resources by `schedule_id`:

    Client.instance().schedules.resources(schedule_id=12345)    

_Note: does not work for capacity type schedules._

#### List Fields of a Schedule

Get all the available fields of a schedule by `schedule_id`:

    Client.instance().schedules.field_list(12345)

#### Create User

Create a user with user attributes params `create(attributes, user_id=None, webhook=None, duplicate=None)`.
If webhook=true is present it will trigger any webhooks connected to the account.
To avoid a ‘create’ action from being automatically interpreted as an ‘update’, you can add the parameter duplicate=raise, then error `422 Unprocessable Entity` will be raised.
If in your database your user has id 1234 then you can supply a foreign key in format 1234fk in `user_id` (optional) which you can use to identify user:
If validation fails for any field then error `422 Unprocessable Entity` will be raised.
Data fields that you can supply can be found [here.](https://www.supersaas.com/info/dev/user_api)

    Client.instance().users.create(attributes={'name': 'name@name.com', 'full_name': 'Example Name', 'email': 'example@example.com'}, user_id=None, webhook=True)

#### Update User

Update a user by `user_id` with user attributes params `update(user_id, attributes, webhook=None, notfound=None)`.
If webhook=true is present it will trigger any webhooks connected to the account.
To avoid automatically creating a new record, you can add the parameter notfound=error or notfound=ignore to return a 404 Not Found or 200 OK respectively.
If the `user_id` does not exist 404 error will be raised.
You only need to specify the attributes you wish to update:

    Client.instance().users.update(user_id=12345, attributes={'full_name': 'New Name'}, true, "ignore")

#### Delete User

Delete a single user by `user_id`, and if the user does not exist 404 error will be raised.:

    Client.instance().users.delete(user_id=12345)
    
#### Get User

Get a single user by `user_id`, and if the user does not exist 404 error will be raised:

    Client.instance().users.get(user_id=12345)

#### List Users

Get all users with optional `form` and `limit`/`offset` pagination params, `list(form=None, limit=None, offset=None)`.
User can have a form attached, and setting `form=True` shows the data:

    Client.instance().users.list(form=False, limit=25, offset=0)

#### List Fields of User object

Get all the fields available to user object:

    Client.instance().users.field_list

#### Create Appointment/Booking

Create an appointment with `schedule_id`, and `user_id(optional)` (see API documentation on [create new](https://www.supersaas.com/info/dev/appointment_api#bookings_api)) appointment attributes and optional `form` and `webhook` params,
`create(schedule_id, user_id, attributes, form=None, webhook=None)`:

    Client.instance().appointments.create(schedule_id=12345, user_id=67890, attributes={'full_name': 'Example Name', 'email': 'example@example.com', 'slot_id': 12345}, form=True, webhook=True)

#### Update Appointment/Booking

Update an appointment by `schedule_id` and `appointment_id` with appointment attributes, see the above link,
`update(schedule_id, appointment_id, attributes, form=None, webhook=None)`:

    Client.instance().appointments.update(schedule_id=12345, appointment_id=67890, attributes={'full_name': 'New Name'}, webhook=True)

#### Delete Appointment/Booking

Delete a single appointment by `schedule_id` and `appointment_id`:

    Client.instance().appointments.delete(schedule_id=12345, appointment_id=67890, webhook=True)

#### Get Appointment/Booking

Get a single appointment by `schedule_id` and `appointment_id`:

    Client.instance().appointments.get(schedule_id=12345, appointment_id=67890)

#### List Appointments/Bookings

List appointments by `schedule_id`, with `form` and `start_time` and `limit` view params `list(schedule_id, form=None, start_time=None, limit=None)`:

    Client.instance().appointments.list(schedule_id=12345, form=True, start_time=datetime.now(), limit=50)

#### Get Agenda

Get agenda (upcoming) appointments by `schedule_id` and `user_id`, with `from_time` view param ([see](https://www.supersaas.com/info/dev/appointment_api#agenda),
`agenda(schedule_id, user_id, from_time=None, slot=False)`:

    Client.instance().appointments.agenda(schedule_id=12345, user_id=67890, from_time=datetime.now())

#### Get Agenda Slots

Get agenda (upcoming) slots by `schedule_id` and `user_id`, with `from_time` view param,
`agenda_slots(schedule_id, user_id, from_time=None)`:

    Client.instance().appointments.agenda_slots(schedule_id=12345, user_id=67890, from_time=datetime.now())

_Note: only works for capacity type schedules._

#### Get Available Appointments/Bookings

Get available appointments by `schedule_id`, with `from_time` time and `length_minutes` and `resource` params ([see](https://www.supersaas.com/info/dev/appointment_api#availability_api),
`available(schedule_id, from_time=None, length_minutes=None, resource=None, full=None, limit=None)`:

    Client.instance().appointments.available(schedule_id=12345, from_time='2018-01-31 00:00:00', length_minutes=15, resource='My Class')

#### Get Recent Changes

Get recently changed appointments by `schedule_id`, with `from_time` time, `to` time, `user` user, `slot` view params (see [docs](https://www.supersaas.com/info/dev/appointment_api#recent_changes)),
`changes(schedule_id, from_time=None, to=None, slot=False, user=None, limit=None, offset=None)`:

    Client.instance().appointments.changes(schedule_id=12345, from_time='2018-01-31 00:00:00', True)

#### Get Recent Changes Slots

Get recently changed slot appointment by `schedule_id`, with `from_time` view params:

    Client.instance().appointments.changes_slots(schedule_id=12345, from_time='2018-01-31 00:00:00')

_Note: only works for capacity type schedules._

#### Get range of appointments

Get range of appointments by `schedule_id`, with `today`,`from_time`, `to` time and `slot` view params (see [docs](https://www.supersaas.com/info/dev/appointment_api#range)),
`range(schedule_id, today=False, from_time=None, to=None, slot=False, user=None, resource_id=None, service_id=None, limit=None, offset=None)`:

    Client.instance().appointments.range(schedule_id=12345, today=True, from_time='2020-01-31 00:00:00',to='2020-02-01 00:00:00' slot=False)

#### List Template Forms

Get all forms by template `superform_id`, with `from_time`, and `user` params ([see](https://www.supersaas.com/info/dev/form_api)),
`list(superform_id, from_time=None, user=None)`:

    Client.instance().forms.list(superform_id=12345, from_time='2018-01-31 00:00:00')

#### Get a list of SuperForms

Get a list of Form templates (SuperForms):

    Client.instance().forms.forms

#### Get Form

Get a single form by `form_id`, will raise 404 error if not found:

    Client.instance().forms.get(form_id=12345)

#### List Promotions

Get a list of promotional coupon codes with pagination parameters `limit` and `offset` (see [docs](https://www.supersaas.com/info/dev/promotion_api)),
`list(limit=None, offset=None)`:

    Client.instance().promotions.list

#### Get a single coupon code

Retrieve information about a single coupon code use with `promotion_code`:

    Client.instance().promotions.promotion(12345)

#### Duplicate promotion code

Duplicate a template promotion by giving (new) `promotion_code` and `template_code` in that order,
`duplicate_promotion_code(self, promotion_code, template_code)`:

    Client.instance().promotions.duplicate_promotion_code(12345, 94832838)

#### List Groups in an account

List Groups in an account ([see](https://www.supersaas.com/info/dev/information_api)):

    Client.instance().groups.list

## Error Handling

The API Client raises a custom Error for HTTP errors and invalid input. Rescue from `SuperSaaS.Error` when making API requests. e.g.

    
    from SuperSaaS import Client, Error
    try:
        Client.instance().users.get
    except Error:
        # Handle error

Validation errors are assigned to the response model. e.g.

    appointment = Client.instance().appointments.create(12345, {bad_field_name: ''})
    appointment.errors #=> [{"status":"400","title":"Bad request: unknown attribute 'bad_field_name' for Booking."}]

## Additional Information

+ [SuperSaaS Registration](https://www.supersaas.com/accounts/new)
+ [Product Documentation](https://www.supersaas.com/info/support)
+ [Developer Documentation](https://www.supersaas.com/info/dev)
+ [Ruby API Client](https://github.com/SuperSaaS/supersaas-ruby-api-client)
+ [PHP API Client](https://github.com/SuperSaaS/supersaas-php-api-client)
+ [NodeJS API Client](https://github.com/SuperSaaS/supersaas-nodejs-api-client)

Contact: [support@supersaas.com](mailto:support@supersaas.com)

## Releases

The package follows [semantic versioning](https://semver.org/), i.e. MAJOR.MINOR.PATCH 

## Development

### Examples
Do not run the examples blindly nor against your production database. They can have destructive effects, so please thread carefully.

### Running tests
Run the pytest command with the path to your test folder. If you run into caching issues, then you either have to turn off the caching for tests or delete `__pycache__` in the test folder. If you wish to run the rate limiter test, you need to set the `SSS_PYTHON_RATE_LIMITER_TEST` environmental variable to `true`. Run all tests:

    $ pytest test/*

or with a specific file:

    $ pytest test/AppointmentsTest.py

## License

The SuperSaaS Python API Client is available under the MIT license. See the LICENSE file for more info.
