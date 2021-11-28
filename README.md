# ProMe

Email: prome.jmoss@gmail.com

Prototype for ProMe app
- Uses `https://developer.mapquest.com/` for maps
- Uses MongoDB Atlas as database
- Other values provided in [config file](ProMeAPI/services/config.py)

```
git clone https://github.com/sairaghav/ProMe
cd ProMe
python -m virtualenv venv
venv\Scripts\activate (for Windows)
source venv/bin/activate (for Linux)
pip install -r requirements.txt

python manage.py runserver
```

## Endpoints

**Unauthenticated APIs**

- `POST /api/auth/users/`: Create new user for accessing the authenticated APIs. Requires `username`, `phone`, `email`, `password` parameters. `first_name` and `last_name` are optional parameters

- `POST /api/auth/token/login/`: Get access token for accessing the authenticated APIs. Requires `username` and `password` parameters


**Authenticated APIs**

*Requires `Authorization: Token <token>` header value*

- `GET /api/directions?start=<source_street>&end=<destination_street>&mode=<mode_of_transport>`: Returns route from source to destination with the mode of transport. `mode` parameter is optional and is *pedestrian* by default. Other possible values are *fastest* and *bicycle*

- `GET /api/getriskdata?street=<street_name>&from=<yyyy-mm-dd>&to=<yyyy-mm-dd>`: Returns all risk data from all sources for the specified street in `street` between the time period specified in `from` and `to`. `from` and `to` are optional parameters and if not given, the time difference is taken as specified in the [config file](ProMeAPI/services/config.py)

- `POST /api/report?street=<street_name>&summary=<summary>&tags=<tags>&user=<user>`: Adds a user reported incident to the risk database


## Example Usage

**Get risk data for one street**

```
import requests

email = ''
password = ''
base_url = 'https://pro-me.herokuapp.com' # Use http://localhost:8000 if you are running locally on port 8000

street = '' # Enter street name here

from_date = '' # Enter date from which news must be evaluated yyyy-mm-dd. Optional
to_date = '' # Enter date till which news must be evaluated yyyy-mm-dd. Optional

if len(from_date) > 0 and len(to_date) > 0:
    params = 'street='+str(street)+'&from='+str(from_date)+'&to='+str(to_date)
else:
    params = 'street='+str(street)

post_data_for_login = {
    'email': email,
    'password': password
}

headers = {
    'Authorization': ''
}
print('Logging in..')
response_data = (requests.post(base_url+'/api/auth/token/login', data=post_data_for_login)).json()
if 'auth_token' in response_data.keys():
    print('Logged in..')
    headers['Authorization'] = 'Token '+str(response_data['auth_token'])
    print('Getting risk data..')
    risk_data = (requests.get(base_url+'/api/getriskdata?'+params, headers=headers)).json()
    print(risk_data)
else:
    print('Some error in login..')
    print(response_data)
```