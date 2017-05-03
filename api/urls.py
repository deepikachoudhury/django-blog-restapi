from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^blogs/$',views.blog_list),
    url(r'^blogs/(?P<pk>[0-9]+)$', views.blog_detail),
]