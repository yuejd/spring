from django.conf.urls import url
from forests import views


urlpatterns = [
    url(
        r'^(?P<switch_id>[0-9]+)/port/(?P<port_index>[0-9]+)$',
        views.SWPortDetail.as_view(),
        name='switch_port_detail'
    ),
]
