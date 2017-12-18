from django.conf.urls import url
from api_prod import views

urlpatterns = [
    url(r'^humanoid/$', views.snippet_list),
    url(r'^detail/(?P<username>\w{0,50})/$$', views.detail),
]