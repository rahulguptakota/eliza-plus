from django.shortcuts import render
from django.http import HttpResponse
import pygeoip
import requests
import json
from bs4 import BeautifulSoup
import urllib2
# Create your views here.
def index(request):
    return HttpResponse("hello world")

def chatpage(request):
#    template = loader.get_template('intpa/chatpage.html')
    context = {}
    return render(request, 'intpa/chatpage.html', context)

def getweather(request):
    client_address = request.META['HTTP_X_FORWARDED_FOR']
    gi = pygeoip.GeoIP('GeoIPCity.dat')
    city = gi.record_by_addr(client_address).city
    weather_data = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+city+'&APPID=b64701c2ef43f513e326906d0ddd0f9f')
    return HttpResponse(json.dumps(weather_data), content_type='application/json');

def googledefine(request):
    keyword = request.GET['define']
    url = "http://www.dictionary.com/browse/"+ keyword +"?s=ts"
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    tabcontent = soup.find('div', {"class": "def-content"})
    m = { 1 : tabcontent.text}
    return HttpResponse(json.dumps(m), content_type='application/json')


def displayimage(request):
    keyword = request.GET['display']
    url = "https://in.images.search.yahoo.com/search/images;?pvid=sb-top-in.images.search.yahoo.com&p="+display
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    x = soup.find_all('img')
    dictionary = {0:x[0]["data-src"],1:x[1]["src"],2:x[2]["data-src"],3x[3]["src"]}
     return HttpResponse(json.dumps(dictionary),content_type='application/json')
        




    
