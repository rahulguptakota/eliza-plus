from django.shortcuts import render
from django.http import HttpResponse
import pygeoip
import requests
import json
from bs4 import BeautifulSoup
import urllib2
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from intpa.forms import ContactForm

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


def googledefine(request):
    keyword = request.POST.get('user_str', False)
    url = "http://www.dictionary.com/browse/"+ str(keyword)+"?s=ts"
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    tabcontent = soup.find('div', {"class": "def-content"})
    m = { 'defn' : str(tabcontent.text)}
    return HttpResponse(json.dumps(m), content_type='application/json')


def photo(request):
    keyword = request.POST.get('user_str', False)	
    url = "https://in.images.search.yahoo.com/search/images;?pvid=sb-top-in.images.search.yahoo.com&p="+keyword
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    x = soup.find_all('img')
    dictionary = {'first':x[0]["data-src"],'second':x[2]["data-src"],'third':x[4]["data-src"],'fourth':x[6]["data-src"]}
    return HttpResponse(json.dumps(dictionary),content_type='application/json')

def send_email(request):
    subject = request.POST.get('subject', '')
    message = request.POST.get('message', '')
    from_email = request.POST.get('from_email', '')
    to_email = request.POST.get('to_email','')
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, to_email)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        #return HttpResponseRedirect('/contact/thanks/')
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse('Make sure all fields are entered and valid.')

def email(request):
    if request.method == 'POST':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            to_email = form.cleaned_data['to_email']
            message = form.cleaned_data['message']
            from_email = form.cleaned_data['from_email']
            try:
                send_mail(subject, message, from_email, [to_email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('thanks')
    return render(request, "intpa/email.html", {'form': form})

def thanks(request):
    return HttpResponse('Thank you for your message.')
