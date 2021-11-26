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