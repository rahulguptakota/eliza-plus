from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'intpa'
urlpatterns = patterns(
    '',
    url(r'^thanks/$',
        views.thanks,
        name='thanks'
        ),
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.LoginFormView.as_view(), name='login'),
    url(r'^chatpage/$', views.chatpage, name='chatpage'),
    url(r'^email/$', views.email, name='email'),
    url(r'^getweather/$', views.getweather, name='getweather'),
    url(r'^googledefine/$', views.googledefine, name='googledefine'),
    url(r'^photo/$', views.photo, name='photo'),
    url(r'^video/$', views.video, name='video'),
    url(r'^registration/$', views.UserFormView.as_view(), name='registration'),
        # url(r'^logout/$', views.LogOut, 'logout')
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
