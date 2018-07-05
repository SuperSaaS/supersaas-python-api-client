# SuperSaaS Python SDK

Online bookings/appointments/calendars in Python using the SuperSaaS scheduling platform - https://supersaas.com

The SuperSaaS API provides services that can be used to add online booking and scheduling functionality to an existing website or CRM software.

## Prerequisites

1. [Register for a (free) SuperSaaS account](https://www.supersaas.com/accounts/new), and
2. get your account name and password. 

##### Dependencies

Python 2.7 or 3.*

No external libraries. The supporting `urllib`/`urllib2` and `json`/`simplejson` standard libs are loaded conditionally.

## Installation

The SDK is available from PyPi and can be installed using pip, e.g.

    $ pip install supersaas-api-client

## Configuration

The `Client` can be used either (1) through the singleton helper method `instance`, e.g.
    
    Client.instance()
    
Or else by (2) simply creating a new client instance manually, e.g.
    
    config = Configuration()
    client = Client(config)

Initialize the SuperSaaS `Client` with authorization credentials:

    from SuperSaaS import Client
    Client.instance().configure(
        account_name = 'accnt'
        password = 'pwd'
    )    
    
> Note, ensure that `configure` is called before `instance`, otherwise the client will be initialized with configuration defaults.

If the client isn't configured explicitly, it will use default `ENV` variables for the account name and password.

    ENV['SSS_API_ACCOUNT_NAME'] = 'your-env-supersaas-account-name'
    ENV['SSS_API_PASSWORD'] = 'your-env-supersaas-account-name' 
    Client.instance().account_name #=> 'your-env-supersaas-account-name'
    Client.instance().password #=> 'your-env-supersaas-account-name'
    
All configuration options can be individually set on the client.

    Client.instance().password = 'pwd' 
    Client.instance().verbose = true
    ...

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

#### Create User

Create a user with user attributes params:

    Client.instance().users.create(attributes={'full_name': 'Example Name', 'email': 'example@example.com, 'slot_id': 12345}, user_id=None, webhook=True)

#### Update User

Update a user by `user_id` with user attributes params:

    Client.instance().users.update(user_id=12345, attributes={'full_name': 'New Name'})

#### Delete User

Delete a single user by `user_id`:

    Client.instance().users.delete(user_id=12345)
    
#### Get User

Get a single user by `user_id`:

    Client.instance().users.get(user_id=12345)

#### List Users

Get all users with optional `form` and `limit`/`offset` pagination params:

    Client.instance().users.list(form=false, limit=25, offset=0)

#### Create Appointment/Booking

Create an appointment by `schedule_id` and `user_id` with appointment attributes and `form` and `webhook` params:

    Client.instance().appointments.create(schedule_id=12345, user_id=67890, attributes={full_name: 'Example Name', email: 'example@example.com', slot_id: 12345}, form=True, webhook=True)

#### Update Appointment/Booking

Update an appointment by `schedule_id` and `appointment_id` with appointment attributes params:

    Client.instance().appointments.update(schedule_id=12345, appointment_id=67890, attributes={full_name: 'New Name'}, webhook=True)

#### Delete Appointment/Booking

Delete a single appointment by `schedule_id` and `appointment_id`:

    Client.instance().appointments.delete(schedule_id=12345, appointment_id=67890)

#### Get Appointment/Booking

Get a single appointment by `schedule_id` and `appointment_id`:

    Client.instance().appointments.get(schedule_id=12345, appointment_id=67890)

#### List Appointments/Bookings

List appointments by `schedule_id`, with `form` and `start_time` and `limit` view param:

    Client.instance().appointments.list(schedule_id=12345, form=true, start_time=datetime.now(), limit=50)

#### Get Agenda

Get agenda (upcoming) appointments by `schedule_id` and `user_id`, with `from_time` view param:

    Client.instance().appointments.agenda(schedule_id=12345, user_id=67890, from_time=datetime.now())

#### Get Agenda Slots

Get agenda (upcoming) slots by `schedule_id` and `user_id`, with `from_time` view param:

    Client.instance().appointments.agenda_slots(schedule_id=12345, user_id=67890, from_time=datetime.now())

_Note: only works for capacity type schedules._

#### Get Available Appointments/Bookings

Get available appointments by `schedule_id`, with `from_time` time and `length_minutes` and `resource` params:

    Client.instance().available(schedule_id12345, from_time='2018-1-31 00:00:00', length_minutes=15, resource='My Class')

#### Get Recent Changes

Get recently changed appointments by `schedule_id`, with `from_time` view param:

    Client.instance().appointments.changes(schedule_id=12345, from_time='2018-1-31 00:00:00', true)

#### Get Recent Changes Slots

Get recently changed slot appointment by `schedule_id`, with `from_time` view params:

    Client.instance().appointments.changes(schedule_id=12345, from_time='2018-1-31 00:00:00')

_Note: only works for capacity type schedules._

#### List Template Forms

Get all forms by template `superform_id`, with `from_time` param:

    Client.instance().forms.list(superform_id=12345, from_time='2018-1-31 00:00:00')

#### Get Form

Get a single form by `form_id`:

    Client.instance().forms.get(form_id=12345)
    
## Error Handling

The API Client raises a custom Error for HTTP errors and invalid input. Rescue from `SuperSaaS.Error` when making API requests. e.g.

    
    from SuperSaaS import Client, Error
    try:
        Client.instance().users.get
    except Error:
        # Handle error
    end

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
+ [C# API Client](https://github.com/SuperSaaS/supersaas-csharp-api-client)
+ [Objective-C API Client](https://github.com/SuperSaaS/supersaas-objc-api-client)
+ [Go API Client](https://github.com/SuperSaaS/supersaas-go-api-client)

Contact: [support@supersaas.com](mailto:support@supersaas.com)

## Releases

The package follows [semantic versioning](https://semver.org/), i.e. MAJOR.MINOR.PATCH 

## License

The SuperSaaS Python API Client is available under the MIT license. See the LICENSE file for more info.
