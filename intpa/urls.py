from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'intpa'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.LoginFormView.as_view(), name='login'),
    url(r'^chatpage/$', views.chatpage, name='chatpage'),
    url(r'^registration/$', views.UserFormView.as_view(), name='registration'),
    url(r'^logout/$', views.LogOut, 'logout')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
