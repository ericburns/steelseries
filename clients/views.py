from django.core.urlresolvers import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

from clients.models import Parent, Retailer


class ParentListView(ListView):
    model = Parent

    def get_queryset(self):
        return self.model.objects.active_tiers()


class ParentDetailView(DetailView):
    model = Parent


class RetailerListView(ListView):
    model = Retailer

    def get_queryset(self):
        return self.model.objects.order_by('name')


class RetailerEditView(UpdateView):
    model = Retailer
    template_name = 'clients/retailer_edit.html'

    def get_success_url(self):
        return reverse('retailers')
