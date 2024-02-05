from fastapi import APIRouter, Depends

from api.utils.weather_utils import get_weather_all, get_weather_details, query_param

router = APIRouter()


@router.get("/weather/all/")
async def weather_all_route(latitude: float, longitude: float):
    return await get_weather_all(latitude, longitude)


@router.get("/weather/choice/")
async def weather_choice_route(
    latitude: float,
    longitute: float,
    air_temperature: bool = Depends(query_param("air_temperature")),
    air_pressure_at_sea_level: bool = Depends(query_param("air_pressure_at_sea_level")),
    cloud_area_fraction: bool = Depends(query_param("cloud_area_fraction")),
    relative_humidity: bool = Depends(query_param("relative_humidity")),
    wind_from_direction: bool = Depends(query_param("wind_from_direction")),
    wind_speed: bool = Depends(query_param("wind_speed")),
):
    return await get_weather_details(
        latitude,
        longitute,
        air_temperature,
        air_pressure_at_sea_level,
        cloud_area_fraction,
        relative_humidity,
        wind_from_direction,
        wind_speed,
    )
