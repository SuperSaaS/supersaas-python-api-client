# SuperSaaS Python SDK

Online bookings/appointments/calendars in Python using the SuperSaaS scheduling platform - https://supersaas.com

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

Set the SuperSaaS `Client` authorization credentials (e.g. with keys/values from system environment) by calling the `configure` method:

    from SuperSaaS.SDK import Client
    Client.instance().configure(
        account_name=ENV['your-env-supersaas-account-name'],
        password = ENV['your-env-supersaas-account-password'],
        user_name = ENV['your-env-supersaas-user-name']
    )

## API Methods

Details of the data structures, parameters, and values can be found on the developer documentation site:

https://www.supersaas.com/info/dev

#### Create User

Create a user with user attributes params:

    Client.instance().users.create({'full_name': 'Example Name', 'email': 'example@example.com, 'slot_id': 12345}, true, true) #=> <SuperSaaS.SDK.Models.User.User>

#### Update User

Update a user by `user_id` with user attributes params:

    Client.instance().users.update(12345, {'full_name': 'New Name'}) #=> {}

## Additional Information

+ [SuperSaaS Registration](https://www.supersaas.com/accounts/new)
+ [Product Documentation](https://www.supersaas.com/info/support)
+ [Developer Documentation](https://www.supersaas.com/info/dev)
+ [Ruby API Client](https://github.com/SuperSaaS/supersaas-ruby-api)
+ [PHP API Client](https://github.com/SuperSaaS/supersaas-php-api)
+ [NodeJS API Client](https://github.com/SuperSaaS/supersaas-nodejs-api)
+ [C# API Client](https://github.com/SuperSaaS/supersaas-csharp-api)
+ [Objective-C API Client](https://github.com/SuperSaaS/supersaas-objc-api)
+ [Go API Client](https://github.com/SuperSaaS/supersaas-go-api)

Contact: [support@supersaas.com](mailto:support@supersaas.com)

## Releases

The gem follows semantic versioning, i.e. MAJOR.MINOR.PATCH 

**MAJOR**releases add or refactor API features and are likely to contain incompatible breaking changes

**MINOR**releases add new backwards-compatible functionality

**PATCH**releases apply backwards-compatible bugfixes or documentation updates

## License

The SuperSaaS Python API Client is available under the MIT license. See the LICENSE file for more info.
