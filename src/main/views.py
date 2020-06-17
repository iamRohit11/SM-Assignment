from django.shortcuts import render
from django.views.generic import ListView, CreateView, TemplateView
from django.urls import reverse,reverse_lazy
from django.http import HttpResponseRedirect,HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import *
from .forms import *
from django.core import serializers
import requests
from .third_party import *
from django.utils import six
from .serializers import MovieSerializer
from datetime import datetime
import json
# Create your views here.

class Homeview(TemplateView):
    template_name='home.html'

class ADWPList(ListView):
    """
    List view for all sources and tags
    """
    queryset = Director.objects.all()
    template_name="attr-upload.html"

    """Adding extra queryset"""
    def get_context_data(self, *args, **kwargs):
        context = super(ADWPList, self).get_context_data(*args, **kwargs)
        # context['qs_2'] = Director.objects.all()
        context['qs_2'] = Writer.objects.all()
        context['qs_3'] = ProductionCompany.objects.all()
        # print(context)
        return context

# class ActorCreate(CreateView):
#     model = Actor
#     form_class = ActForm
#     success_url = reverse_lazy("")
#     template_name = ".html"

def MovieCreate(request):
    if request.POST:
        print(request.POST)
        director = Director.objects.get(pk=request.POST['director'])
        writer = Writer.objects.get(pk=request.POST['writer'])
        prodcom = ProductionCompany.objects.get(pk=request.POST['prodcom'])
        address = {
            'Locality' : request.POST['locality'],
            'City' : request.POST['city'],
            'State' : request.POST['state'],
            'Country' : request.POST['country']
        }
        loc_id = get_location_id(request.POST['country'],request.POST['city'])
        # current = get_curr_cond(loc_id)
        # curr = {
        #     'text': current['WeatherText'],
        #     'raining' : current["PrecipitationSummary"]['Precipitation']['Metric']['Value'],
        #     'rain-type': current['PrecipitationType'],
        #     'temperature': current['Temperature']['Metric']['Value'],
        #     'real-feel' : current['RealFeelTemperature']['Metric']['Value'],
        #     'rel-humidity' : current['RelativeHumidity'],
        #     'wind-dir' : current['Wind']['Direction']['English'],
        #     'wind-speed' : current['Wind']['Speed']['Metric']['Value'],
        #     'visibility' : current['Visibility']['Metric']['Value']
        # }
        ins = Movie.objects.create(released=request.POST['year'],title=request.POST['title'],
        writer=writer,director=director,address=address,location_id=loc_id,produced_by=prodcom)
        ins.save()
        return HttpResponseRedirect(reverse_lazy("Home"))

    context = {
        # 'actor': Actor.objects.all(),
        'writer': Writer.objects.all(),
        'director': Director.objects.all(),
        'prodcom' : ProductionCompany.objects.all(),
        'country' : Countrie.objects.all()
    }

    return render(request,'Movie-create.html',context)

def LocSearch(request):
    context = {
        'movies': Movie.objects.all()
    }
    return render(request,'loc-search.html',context)

@api_view(['GET'])
def search_results(request):
    try:
        get_dict = dict(six.iterlists(request.GET))
        mpks = get_dict['mv[]']
        movies = Movie.objects.none()
        for i in mpks:
            movies |= Movie.objects.filter(id=i)
        serializer = MovieSerializer(movies, many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    except:
        return Response(data={},status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def current_weather(request):
    movie_obj = Movie.objects.get(id=request.GET['id'])
    loc_id = movie_obj.location_id
    if movie_obj.modified_at :
        pass
    api_data = get_curr_cond(loc_id)
    curr_cond = {
        'text': api_data['WeatherText'],
        'raining' : api_data["PrecipitationSummary"]['Precipitation']['Metric']['Value'],
        'rain_type': api_data['PrecipitationType'],
        'temperature': api_data['Temperature']['Metric']['Value'],
        'real_feel' : api_data['RealFeelTemperature']['Metric']['Value'],
        'rel_humidity' : api_data['RelativeHumidity'],
        'wind_dir' : api_data['Wind']['Direction']['English'],
        'wind_speed' : api_data['Wind']['Speed']['Metric']['Value'],
        'visibility' : api_data['Visibility']['Metric']['Value']
    }
    return Response(data=curr_cond,status=status.HTTP_200_OK)

@api_view(['GET'])
def forecasted_weather(request):
    try:
        movie_obj = Movie.objects.get(id=request.GET['id'])
        loc_id = movie_obj.location_id
        api_data = get_forecast(loc_id)
        forecast = {
            'rainfall' : api_data['Precipitation']
        }
        return Response(data=forecast,status=status.HTTP_200_OK)
    except:
        return Response(data=api_data,status=status.HTTP_404_NOT_FOUND)