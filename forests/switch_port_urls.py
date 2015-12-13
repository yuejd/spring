from django.conf.urls import url
from forests import views


urlpatterns = [
    url(
        r'^(?P<pk>[0-9]+)$',
        views.SWPortDetail.as_view(),
        name='switch_port_detail'
    ),
    url(
        r'^(?P<pk>[0-9]+)/(?P<action>\w+)$',
        views.SWPortAction.as_view(),
        name='switch_port_action'
    ),
]
