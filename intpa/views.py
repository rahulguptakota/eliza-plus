from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserForm
from django import forms
from django.views import generic


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
	client_address = request.META['HTTP_X_FORWARDED_FOR']
	gi = pygeoip.GeoIP('GeoIPCity.dat')
	city = gi.record_by_addr(client_address).city
	r = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+city+'&APPID=b64701c2ef43f513e326906d0ddd0f9f')
	weather_data = r.json()
	return HttpResponse(json.dumps(weather_data), content_type='application/json');


class UserFormView(generic.DetailView):

	form_class = UserForm
	template_name = 'intpa/regForm.html'

#display blank form
	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form': form})

#process form data
	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():

			user = form.save(commit=False)

#cleaned (normalized ) data
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()
