from django.conf.urls import url
from . import views

app_name='mhclient'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(),name="index"),
    url(r'^(?P<human_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^human/add$', views.HumanoidCreate.as_view(), name='human-add'),
    url(r'^(?P<human_id>[0-9]+)/humanoidedit$', views.HumanoidEdit.as_view(), name='humanoidedit'),
    url(r'^(?P<human_id>[0-9]+)/delete$', views.deleteobj, name='deleteobj'),
]