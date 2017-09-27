from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name = 'dashboard'),
    url(r'^destination/(?P<trip_id>\d+)$', views.destination, name = 'destination'),
    url(r'^trip/join/process/(?P<trip_id>\d+)$', views.join_trip, name = 'join_trip'),
    url(r'^add$', views.add_travel, name = 'add_travel'),
    url(r'^add/process$', views.process_add_travel, name = 'process_add_travel'),
]
