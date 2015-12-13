from django.conf.urls import url
from forests import views


urlpatterns = [
    url(r'^$', views.server_list, name='server_list'),
    url(r'^(?P<server_id>[0-9]+)$',
        views.ServerDetail.as_view(),
        name='server_detail'),
    url(r'^(?P<server_id>[0-9]+)/resync',
        views.server_resync,
        name='server_resync'),
]
