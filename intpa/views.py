from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, LoginForm
from django import forms
from django.views import generic
from django.views.generic import View
from django.urls import reverse
# import gnp
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from intpa.forms import ContactForm
import pygeoip
import requests
import json
from bs4 import BeautifulSoup
import urllib.request as urllib
from django.core.mail import send_mail, BadHeaderError
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


def googledefine2(request):
    keyword = request.POST.get('user_str', False)
    url = "https://en.wikipedia.org/wiki/"+ str(keyword)
    page = urllib.urlopen(url)
    soup = BeautifulSoup(page)
    tabcontent = soup.find_all('div', {"id": "mw-content-text"})
    m = { 'p' : str(tabcontent.text)}
    return HttpResponse(json.dumps(m), content_type='application/json')

# def news(request):
# 	keyword = request.POST.get('user_str', False)
# 	a = gnp.get_google_news(gnp.EDITION_ENGLISH_INDIA)
# 	if(keyword == False or keyword==""):
# 		keyword="Top Stories"
# 	topics = [
#         "Top Stories", 
#         "Kanpur", 
#         "India", 
#         "World", 
#         "Business", 
#         "Technology", 
#         "Entertainment", 
#         "Sports", 
#         "Science", 
#         "Health", 
#         "More Top Stories"
#     ]
# 	i=0
# 	for str in topics:
# 		if(str.lower()==keyword.lower()):
# 			break
# 		i = i + 1
# 	i=i-1
# 	if(i<0):
# 		i=0
	
# 	data = []
# 	for j in range(5):
# 		data.append(a["stories"][j+20*i])
# 	return HttpResponse(json.dumps({"news":data}), content_type='application/json')

def googledefine(request):
    print(request.POST.dict())
    keyword = request.POST.get('user_str', False)
    url = "http://www.dictionary.com/browse/"+ keyword +"?s=ts"
    page = urllib.urlopen(url)
    soup = BeautifulSoup(page)
    tabcontent = soup.find('div', {"class": "def-content"})
    m = { 1 : tabcontent.text}
    return HttpResponse(json.dumps(m), content_type='application/json')

def photo(request):
    keyword = request.POST.get('user_str', False)	
    url = "https://in.images.search.yahoo.com/search/images;?pvid=sb-top-in.images.search.yahoo.com&p="+keyword
    page = urllib.urlopen(url)
    soup = BeautifulSoup(page)
    x = soup.find_all('img')
    dictionary = {'first':x[0]["data-src"],'second':x[2]["data-src"],'third':x[4]["data-src"],'fourth':x[6]["data-src"]}
    return HttpResponse(json.dumps(dictionary),content_type='application/json')

def video(request):
    keyword = request.POST.get('user_str', False)	
    url = "https://in.video.search.yahoo.com/search/video?pvid=sb-top-in.video.search.yahoo.com&p="+keyword+"&vsite=youtube"
    page = urllib.urlopen(url)
    soup = BeautifulSoup(page)
    x = soup.find("a",{"class":"ng"})
    desr = str(x["data-rurl"])
    desr = desr.replace("watch?v=","embed/")
    
    y = {'url': desr}
    return HttpResponse(json.dumps(y),content_type='application/json')
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
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            to_email = form.cleaned_data['to_email']
            try:
                send_mail(subject, message, "", [to_email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponse('Email has been sent.')
    return render(request, "intpa/email.html", {'form': form})

def thanks(request):
    return HttpResponse('Email has been sent.')

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
