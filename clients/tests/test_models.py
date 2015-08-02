import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from clients.models import Parent, Retailer


class ParentTest(TestCase):

    def test_tiers(self):
        now = datetime.datetime.now().date()
        two_days_ago = now - datetime.timedelta(days=2)
        five_days_ago = now - datetime.timedelta(days=5)

        parent = Parent.objects.create(
            name='Parent',
            country='Country',
            tier='Tier 1',
            start_date=two_days_ago
        )

        Parent.objects.create(
            name='Parent',
            country='Country',
            tier='Tier 2',
            start_date=now
        )

        Parent.objects.create(
            name='Parent',
            country='Country',
            tier='Tier 2',
            start_date=five_days_ago
        )

        expected = [
            {
                'tier': u'Tier 2',
                'start_date': now
            },
            {
                'tier': u'Tier 1',
                'start_date': two_days_ago
            },
            {
                'tier': u'Tier 2',
                'start_date': five_days_ago
            }
        ]

        self.assertSequenceEqual(parent.tiers(), expected)


class ParentManagerTest(TestCase):

    def test_active_tiers(self):
        """
        Make sure only the parent with the most recent start_date is returned.
        """
        now = datetime.datetime.now().date()

        Parent.objects.create(
            name='Parent',
            country='Country',
            tier='Tier 1',
            start_date=now - datetime.timedelta(days=2)
        )

        p2 = Parent.objects.create(
            name='Parent',
            country='Country',
            tier='Tier 2',
            start_date=now
        )

        tiers = list(Parent.objects.active_tiers())

        self.assertEqual(len(tiers), 1)
        self.assertEqual(tiers[0].start_date, p2.start_date)
