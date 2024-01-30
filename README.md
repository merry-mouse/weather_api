# Weather API

This is a simple weather API that was built using FastAPI. It uses official [YR API](https://api.met.no/weatherapi/locationforecast/2.0/documentation) to retrieve information about the weather in a special area by providing its altitude, longtitude and the parameters that user wants to know about including:

- air_temperature,
- air_pressure_at_sea_level
- cloud_area_fraction
- relative_humidity
- wind_from_direction
- wind_speed

## Installation

After cloning this repo to your local machine you need to activate Python virtual environment that can be done using this command where .new_venv is the name for the nvironment. You can use a different name (all commands are for Mac/Linux):

```
python3 -m venv .new_venv
```

After creating your virtual environment you need to activate it
(assuming you are in directory where .new_venv located):

```
source .new_venv/bin/act
```

Then install all the packages from the requirements.txt using this command:

```
pip install -r requirements.txt
```

## Usage

### Identification at YR API

All requests must (if possible) include an identifying User Agent-string (UA) in the request with the application/domain name, optionally version number. You should also include a company email address or a link to the company website where we can find contact information. If we cannot contact you in case of problems, you risk being blocked without warning.

Examples of valid User-Agents:

- "acmeweathersite.com support@acmeweathersite.com"
- "AcmeWeatherApp/0.9 github.com/acmeweatherapp"

In order to initialize a request to YR API, you need to have a [Useragent](https://docs.api.met.no/doc/locationforecast/HowTO.html) object, with a custom User-Agent request header using the sitename variable as value. If this is missing or generic, you will get a 403 Forbidden response.
This weather API expects you to have Useragent stored at the _config.py_ file. It should be located in the root directory, contain Project Name, its version and sitename (can be your github account) and should look somewhat like this:

#### config.py

```
USER_AGENT = "ProjectName/0.0.1 github.com/my-account"
```

When config.py was created you can start using API. Run the serverfrom the root directory with this command:

```
uvicorn api.main:app --reload
```

If everything is fine you will see these line appeared in your terminal:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [18245] using StatReload
INFO:     Started server process [18247]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:62903 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:62903 - "GET /openapi.json HTTP/1.1" 200 OK
```

If you see that server is running without any error, you can check out the API using Swagger docs UI. For this go to http://127.0.0.1:8000/docs

There you suppose to see 2 endpoints:

1.  GET /weather/all

This endpoint provides you all the info with the forecast for the upcoming week and you cannot choose which parameters you want unlike in the second endpoint. There are only 2 parameters that are required which are latitude and longtitude.

2. GET /weather/choice

As name suggests, at this endpoint you can choose which parameters you are interested in to see in the forecast. Lattitude and longtitude are required but you can also choose what kind of forecast you want by setting these parameters to true:

- air_temperature
- air_pressure_at_sea_level
- cloud_area_fraction
- relative_humidity
- wind_from_direction
- wind_speed

With Swagger UI, just put in your coordinates, set to true optional parameters you are interested in and get your response, as easy as that!

And if you want to use curl you can use this command while uvicorn server is running:

```
curl -X 'GET' \
  'http://127.0.0.1:8000/weather/choice/?latitude=00.0000&longtitude=00.00000&air_temperature=true' \
  -H 'accept: application/json'
```

And if you use something like Postman, send GET request to [http://127.0.0.1:8000/weather/choice/?latitude=00.000000&longtitude=00.000000&air_temperature=true](http://127.0.0.1:8000/weather/choice/?latitude=59.256569&longtitude=17.881121&air_temperature=true) with "lat", "lon" as required and other optional (air_temperature in this example) parameters.

## Response data

This is how the response data is structured:

```
{
    "timeseries": {
        "2024-01-30": [
            {
                "time": "14:00:00",
                "air_temperature": 3.3
            },
            {
                "time": "15:00:00",
                "air_temperature": 3.2
            },
            {
                "time": "16:00:00",
                "air_temperature": 3.1
            },
            {
                "time": "17:00:00",
                "air_temperature": 3.3
            },
            {
                "time": "18:00:00",
                "air_temperature": 3.3
            },
            {
                "time": "19:00:00",
                "air_temperature": 3.4
            },
            {
                "time": "20:00:00",
                "air_temperature": 3.4
            },
            {
                "time": "21:00:00",
                "air_temperature": 3.5
            },
            {
                "time": "22:00:00",
                "air_temperature": 3.9
            },
            {
                "time": "23:00:00",
                "air_temperature": 3.4
            }
        ],
        "2024-01-31": [
            {
                "time": "00:00:00",
                "air_temperature": 3.2
            },
            {
                "time": "01:00:00",
                "air_temperature": 3.1
            },
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
