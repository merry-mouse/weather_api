from collections import defaultdict

import httpx
from fastapi import HTTPException, Query

from config import USER_AGENT

YR_API_URL = "https://api.met.no/weatherapi/locationforecast/2.0/compact"


def query_param(param_name: str):
    def inner_query_param(value: bool = Query(None, alias=param_name)):
        return value is not None

    return inner_query_param


async def get_weather_all(latitude: float, longitude: float):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                YR_API_URL,
                params={"lat": latitude, "lon": longitude},
                headers={"User-Agent": USER_AGENT},
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=str(e),
            )


async def get_weather_details(
    latitude: float,
    longitude: float,
    air_temperature: bool = False,
    air_pressure_at_sea_level: bool = False,
    cloud_area_fraction: bool = False,
    relative_humidity: bool = False,
    wind_from_direction: bool = False,
    wind_speed: bool = False,
):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                YR_API_URL,
                params={"lat": latitude, "lon": longitude},
                headers={"User-Agent": USER_AGENT},
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=404,
                    detail="Weather data not found",
                )
            else:
                response_data = response.json()
                chosen_details = {
                    "air_pressure_at_sea_level": air_pressure_at_sea_level,
                    "air_temperature": air_temperature,
                    "cloud_area_fraction": cloud_area_fraction,
                    "relative_humidity": relative_humidity,
                    "wind_from_direction": wind_from_direction,
                    "wind_speed": wind_speed,
                }
                chosen_detail_keys = [
                    key for key, value in chosen_details.items() if value
                ]
                formatted_data = flatten_weather_data(
                    response_data,
                    chosen_detail_keys,
                )

            return {"timeseries": formatted_data}

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=str(e),
            )


def flatten_weather_data(response_data, chosen_details):
    # Initialize a defaultdict to hold lists of entries for each date
    formatted_data = defaultdict(list)

    # Loop through each entry in the timeseries
    for timeseries_entry in response_data["properties"]["timeseries"]:
        # Extract the timestamp and split into date and time
        timestamp = timeseries_entry["time"]
        date, time = timestamp.split("T")
        time = time[:-1]  # Remove the 'Z' at the end

        # Create a dictionary entry for the time and relevant details
        entry = {"time": time}
        details = timeseries_entry["data"]["instant"]["details"]

        # Add chosen details to the entry
        for detail in chosen_details:
            if detail in details:
                entry[detail] = details[detail]

        # Append the entry to the list for the corresponding date
        formatted_data[date].append(entry)

    # Convert the defaultdict to a regular dictionary for JSON serialization
    return dict(formatted_data)
