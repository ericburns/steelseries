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
