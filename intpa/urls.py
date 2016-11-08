from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = patterns(
    '',
    url(r'^email/$',
        views.email,
        name='email'
        ),
    url(r'^thanks/$',
        views.thanks,
        name='thanks'
        ),
    url(r'^$', views.index, name='index'),
    url(r'^chatpage/$', views.chatpage, name='chatpage'),
    url(r'^email/$', views.email, name='email'),
    url(r'^getweather/$', views.getweather, name='getweather'),
    url(r'^googledefine/$', views.googledefine, name='googledefine'),
    url(r'^photo/$', views.photo, name='photo'),
    url(r'^video/$', views.video, name='video'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
