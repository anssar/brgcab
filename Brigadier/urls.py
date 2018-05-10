"""
Definition of urls for Brigadier.
"""

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

from Brigadier.brigadier import views

admin.autodiscover()

urlpatterns = [
    url(r'^$', views.login),
    url(r'^login/$', views.login),
    url(r'^signin$', views.signin),
    url(r'^load/$', views.load),
    url(r'^load$', views.load),
    url(r'^loading$', views.loading),
    url(r'^login/signin$', views.signin),
    url(r'^signout/$', views.signout),
    url(r'^drivers/$', views.drivers),
    url(r'^drivers-online/$', views.drivers_online),
    url(r'^create_driver/$', views.make_driver),
    url(r'^create_driver/create$', views.create),
    url(r'^drivers/driver/(?P<crew_pk>\d+)/$', views.driver),
    url(r'^drivers-online/driver/(?P<crew_pk>\d+)/$', views.driver),
    url(r'^drivers-online/driver/(?P<crew_pk>\d+)/save$', views.saveName),
    url(r'^drivers-online/driver/(?P<crew_pk>\d+)/change$', views.changeCar),
    url(r'^drivers-online/driver/(?P<crew_pk>\d+)/regenerate$', views.regeneratePassword),
    url(r'^drivers/driver/(?P<crew_pk>\d+)/save$', views.saveName),
    url(r'^drivers/driver/(?P<crew_pk>\d+)/change$', views.changeCar),
    url(r'^drivers/driver/(?P<crew_pk>\d+)/regenerate$', views.regeneratePassword),
    url(r'^drivers/driver/(?P<crew_pk>\d+)/exist$', views.changeExistCar),
    url(r'^drivers/driver/(?P<crew_pk>\d+)/new$', views.changeNewCar),
    url(r'^drivers-online/driver/(?P<crew_pk>\d+)/exist$', views.changeExistCar),
    url(r'^drivers-online/driver/(?P<crew_pk>\d+)/new$', views.changeNewCar),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin', include(admin.site.urls)),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico')),
]

handler404 = views.nopage
