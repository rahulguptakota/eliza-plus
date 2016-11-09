from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, LoginForm
from django import forms
from django.views import generic
from django.views.generic import View
from django.urls import reverse

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

def news(request):
	keyword = request.POST.get('user_str', False)
	a = gnp.get_google_news(gnp.EDITION_ENGLISH_INDIA)
	if(keyword == False):
		keyword="Top Stories"
	topics = [
        "Top Stories", 
        "Kanpur, Uttar Pradesh", 
        "India", 
        "World", 
        "Business", 
        "Technology", 
        "Entertainment", 
        "Sports", 
        "Science", 
        "Health", 
        "More Top Stories"
    ]
	i=0
	for str in topics:
		if(str==keyword):
			break
		i = i + 1
	
	data = []
	for j in range(20):
		data.append(a["stories"][j+20*i])
	return HttpResponse(json.dumps({"news":data}), content_type='application/json')

def getweather(request):
	client_address = request.META['HTTP_X_FORWARDED_FOR']
	gi = pygeoip.GeoIP('GeoIPCity.dat')
	city = gi.record_by_addr(client_address).city
	r = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+city+'&APPID=b64701c2ef43f513e326906d0ddd0f9f')
	weather_data = r.json()
	return HttpResponse(json.dumps(weather_data), content_type='application/json');


class UserFormView(View):

	form_class = UserForm
	template_name = 'intpa/regForm.html'

#display blank form
	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form': form})

#process form data
	def post(self, request):
		form = self.form_class(request.POST)
		# return HttpResponse(form.is_valid())
		if form.is_valid():
			user = form.save(commit=False)

#cleaned (normalized ) data
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()
		
		# else:
		# 	username = form.cleaned_data['username']
		# 	password = form.cleaned_data['password']
		#return user creditionals if they are correct
			user = authenticate(username=username, password=password)
			
			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect('intpa:chatpage')
		return render(request, self.template_name, {'form': form})



class LoginFormView(View):
	Loginform_class = LoginForm
	template_name = 'intpa/loginForm.html'

	def get(self, request):
		form = self.Loginform_class(None)
		return render(request, self.template_name, {'form': form})

	def post(self, request):
		form = self.Loginform_class(request.POST)
		# return HttpResponse(form.is_valid())
		if 1 :
#cleaned (normalized ) data
			password = request.POST.get("password", False)
			# user_name = request.POST.get("user_name", False)
			gurkirat = request.POST.get("gurkirat", False)
					
		# else:
		# 	username = form.cleaned_data['username']
		# 	password = form.cleaned_data['password']
		#return user creditionals if they are correct
			# return HttpResponse("gurkirat: {} user_name: {} password: {}".format(gurkirat, "removed",password))
			user = authenticate(username=gurkirat, password=password)
			# return HttpResponse(user)
			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect('intpa:chatpage')
		return render(request, self.template_name, {'form': form})

# def LogOut(request):
# 	logout(request)
	# return redirect('intpa:login')
