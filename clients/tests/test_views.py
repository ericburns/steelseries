import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from clients.models import Parent, Retailer


class ParentListViewTest(TestCase):

    def setUp(self):
        self.client = Client()

        self.name = 'Parent {num}'

        for x in xrange(5):
            Parent.objects.create(
                name=self.name.format(num=x),
                country='Country',
                tier='Tier 1',
                start_date=datetime.datetime.now()
            )

    def test_get(self):
        response = self.client.get(reverse('parents'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tier 1', count=5)

    def test_no_duplicate_names(self):
        """
        The Parent table has duplicate names, but we don't want to show duplicates
        in the list view.
        """
        Parent.objects.create(
            name='Parent 0',
            country='Country',
            tier='Tier 1',
            start_date=datetime.datetime.now()
        )

        response = self.client.get(reverse('parents'))
        self.assertContains(response, 'Tier 1', count=5)


class ParentDetailViewTest(TestCase):

    def setUp(self):
        self.client = Client()

        self.parent = Parent.objects.create(
            name='Parent',
            country='Country',
            tier='Tier 1',
            start_date=datetime.datetime.now()
        )

    def test_get(self):
        response = self.client.get(reverse('parent_detail', kwargs={'pk': self.parent.pk}))
        self.assertEqual(response.status_code, 200)


class RetailerListViewTest(TestCase):

    def setUp(self):
        self.client = Client()

        self.name = 'Retailer {num}'

        for x in xrange(5):
            Retailer.objects.create(
                name=self.name.format(num=x),
                parent_name='Parent Name',
                country='Country'
            )

    def test_get(self):
        response = self.client.get(reverse('retailers'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Parent Name', count=5)


class RetailerEditViewTest(TestCase):

    def setUp(self):
        self.client = Client()

        self.parent = Parent.objects.create(
            name='Parent',
            country='Country',
            tier='Tier 1',
            start_date=datetime.datetime.now()
        )

        self.retailer = Retailer.objects.create(
            name='Retailer',
            parent_name=self.parent.name,
            country=self.parent.country,
        )

    def test_get(self):
        response = self.client.get(reverse('retailer_edit', kwargs={'pk': self.retailer.pk}))
        self.assertEqual(response.status_code, 200)

    def test_post_valid_parent_select(self):
        """
        Ensure posting a valid parent_name update updates a Retailers parent_name
        """
        parent2 = Parent.objects.create(
            name='Parent 2',
            country='Country',
            tier='Tier 1',
            start_date=datetime.datetime.now()
        )

        self.assertEqual(self.retailer.parent_name, self.parent.name)

        self.client.post(
            reverse('retailer_edit', kwargs={'pk': self.retailer.pk}),
            {'parent_name': parent2.name})

        retailer = Retailer.objects.get(pk=self.retailer.pk)

        self.assertEqual(retailer.parent_name, parent2.name)

    def test_post_invalid_parent_select(self):
        """
        Ensure posting a parent_name that doens't exist in the parent table fails.
        """
        invalid_choice = 'Invalid Parent Name'

        response = self.client.post(
            reverse('retailer_edit', kwargs={'pk': self.retailer.pk}),
            {'parent_name': invalid_choice})

        err_msg = 'Select a valid choice. {invalid_choice} is not one of the available choices.'.format(
            invalid_choice=invalid_choice)

        self.assertContains(response, err_msg)

        retailer = Retailer.objects.get(pk=self.retailer.pk)

        self.assertEqual(retailer.parent_name, self.retailer.parent_name)
