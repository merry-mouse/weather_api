from typing import Optional

import httpx
from fastapi import FastAPI, HTTPException, Query

from config import USER_AGENT

app = FastAPI()

YR_API_URL = "https://api.met.no/weatherapi/locationforecast/2.0/compact"


@app.get("/weather/all/")
async def get_weather_all(latitude: float, longtitude: float):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                YR_API_URL,
                params={"lat": latitude, "lon": longtitude},
                headers={"User-Agent": USER_AGENT},
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=str(e),
            )


@app.get("/weather/choice/")
async def get_weather_details(
    latitude: float,
    longtitude: float,
    air_pressure_at_sea_level: Optional[bool] = Query(
        None, alias="airPressureAtSeaLevel"
    ),
    air_temperature: Optional[bool] = Query(None, alias="airTemperature"),
    cloud_area_fraction: Optional[bool] = Query(None, alias="cloudAreaFraction"),
    relative_humidity: Optional[bool] = Query(None, alias="relativeHumidity"),
    wind_from_direction: Optional[bool] = Query(None, alias="windFromDirection"),
    wind_speed: Optional[bool] = Query(None, alias="windSpeed"),
):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                YR_API_URL,
                params={"lat": latitude, "lon": longtitude},
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
            raise HTTPException(status_code=e.response.status_code, detail=str(e))


def flatten_weather_data(response_data, choisen_details):
    flatterened_data = []
    for timeseries_entry in response_data["properties"]["timeseries"]:
        entry = {"time": timeseries_entry["time"]}
        details = timeseries_entry["data"]["instant"]["details"]
        for detail in choisen_details:
            if detail in details:
                entry[detail] = details[detail]
        flatterened_data.append(entry)
    return flatterened_data


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
