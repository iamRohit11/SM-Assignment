from django.urls import path,include
from .views import *

urlpatterns = [
    path('',Homeview.as_view(), name="Home"),
    path('add-movie/',MovieCreate, name="Add_movie"),
    path('results/',search_results, name="search-results"),
    path('search/',LocSearch, name="Loc-search"),
    path('conditions/', current_weather, name="curr-weather"),
    path('forecast/', forecasted_weather, name="forecast-weather")
]