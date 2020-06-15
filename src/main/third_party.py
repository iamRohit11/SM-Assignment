import requests
ACCUWEATHER_KEY = "0K7d1Aq4ZFYXeJ30IV1IQlGq4QMViIvj"

def get_location_id(code,city):
    endpoint = 'http://dataservice.accuweather.com/locations/v1/cities/{code}/search?apikey=0K7d1Aq4ZFYXeJ30IV1IQlGq4QMViIvj&q={c}'
    url = endpoint.format(code=code,c=city)
    response = requests.get(url)
    data = response.json()[0]
    return data["Key"]

def get_curr_cond(loc_id):
    endpoint = 'http://dataservice.accuweather.com/currentconditions/v1/{id}/?apikey=0K7d1Aq4ZFYXeJ30IV1IQlGq4QMViIvj&details=true'
    url = endpoint.format(id = loc_id)
    response = requests.get(url)
    data = response.json()[0]
    return data


def get_forecast(loc_id):
    endpoint = 'http://dataservice.accuweather.com/forecasts/v1/daily/1day/{id}/?apikey=0K7d1Aq4ZFYXeJ30IV1IQlGq4QMViIvj'
    url = endpoint.format(id = loc_id)
    response = requests.get(url)
    data = response.json()
    return data