import requests
import json

from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY

# url = ""
# headers = {"Authorization": PEXELS_API_KEY}


# url = ""
# headers = {"Authorization": PEXELS_API_KEY}


def get_photo(city, state):
    # to use the state and city names in the request
    url = "https://api.pexels.com/v1/search"
    params = {
        "per_page": 1,
        "query": city + " " + state,
    }
    headers = {"Authorization": PEXELS_API_KEY}
    # example response from pexel documentation page
    # requests.get(url, params=params, headers=headers)
    response = requests.get(url, params=params, headers=headers)
    content = json.loads(response.content)
    # to filter out the neeeds of us

    try:
        return {"picture_url": content["photos"][0]["src"]["original"]}
    except (KeyError):
        return {"picture_url": None}

    # #  GET https://api.pexels.com/v1/photos/:id
    # response = requests.get("https://api.pexels.com/v1/")
    # picture = json.loads(response.content)
    # # Create a dictionary of data to use ?
    # city_pictures = {"
    #                  "id": picture.["id"],}


def get_weather_data(city, state):
    geo_url = "http://api.openweathermap.org/geo/1.0/direct"
    print(city, state)
    params = {
        "q": city + "," + state,
        "limit": 1,
        "appid": OPEN_WEATHER_API_KEY,
    }
    # pexel documentation da bu vardi, geo da yok.
    # headers = {"Authorization": OPEN_WEATHER_API_KEY}
    #  geo_response = requests.get(geo_url, params=params, headers=headers)
    geo_response = requests.get(geo_url, params=params)
    geo_content = json.loads(geo_response.content)
    print(geo_content)
    lat, lon = geo_content[0]["lat"], geo_content[0]["lon"]
    # return {"geo_url": content["name"]["country"]}

    weather_url = "https://api.openweathermap.org/data/2.5/weather"
    weather_params = {
        "lat": lat,
        "lon": lon,
        "appid": OPEN_WEATHER_API_KEY,
        "units": "imperial",
    }
    weather_response = requests.get(url=weather_url, params=weather_params)

    weather_data = json.loads(weather_response.content)
    temperature = weather_data["main"]["temp"]
    description = weather_data["weather"][0]["description"]
    weather_dict = {"temperature": temperature, "description": description}
    return weather_dict
