"""steelseries URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url

from clients.views import (
    ParentListView,
    ParentDetailView,
    RetailerListView,
    RetailerEditView
)

from clients.forms import RetailerForm


urlpatterns = [
    url(r'^parent/$', ParentListView.as_view(), name='parents'),
    url(r'^parent/(?P<pk>[0-9]+)/$', ParentDetailView.as_view(), name='parent_detail'),

    url(r'^retailer/$', RetailerListView.as_view(), name='retailers'),
    url(r'^retailer/(?P<pk>[0-9]+)/$', RetailerEditView.as_view(form_class=RetailerForm), name='retailer_edit'),
]
