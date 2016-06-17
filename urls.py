from django.conf.urls import url

from . import views

app_name = 'slib'

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^holdings/$', views.HoldingList.as_view(), name = 'holdingslist'),
    url(r'^holdings/(?P<pk>[0-9]+)/$', views.HoldingDetail.as_view(), name = 'holdingsdetail'),
    url(r'^items/$', views.ItemList.as_view(), name = 'itemslist'),
    url(r'^items/(?P<pk>[0-9]+)/$', views.ItemDetail.as_view(), name = 'itemsdetail'),
]