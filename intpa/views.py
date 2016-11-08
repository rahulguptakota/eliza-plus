from django.shortcuts import render
from django.http import HttpResponse
import pygeoip
import requests
import json
# Create your views here.
def index(request):
    return HttpResponse("hello world")

def chatpage(request):
#    template = loader.get_template('intpa/chatpage.html')
    context = {}
    return render(request, 'intpa/chatpage.html', context)

def getweather(request):
    #client_address = request.META['HTTP_X_FORWARDED_FOR']
    client_address = "103.246.106.9"
    #gi = pygeoip.GeoIP('GeoLiteCity.dat')
    #print client_address
    #city = gi.record_by_addr(client_address)['city']
#    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+str(city)+'&APPID=b64701c2ef43f513e326906d0ddd0f9f')
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+'Kanpur'+'&APPID=b64701c2ef43f513e326906d0ddd0f9f')
    weather_data = r.json()
    return HttpResponse(json.dumps(weather_data), content_type='application/json');
