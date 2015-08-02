from django.db import models


class ParentQuerySet(models.QuerySet):

    def active_tiers(self):
        """
        Return the Parent rows representing the currently active tiers.
        """
        return self.raw(
            """
            SELECT * FROM (
                SELECT
                    *
                FROM
                    clients_parent
                ORDER BY
                    start_date ASC
            ) GROUP BY name
            """
        )


class ParentManager(models.Manager):

    def get_queryset(self):
        return ParentQuerySet(self.model, using=self._db)

    def active_tiers(self):
        return self.get_queryset().active_tiers()


class Parent(models.Model):
    country = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    tier = models.CharField(max_length=32, null=True)
    start_date = models.DateField()
    objects = ParentManager()

    def tiers(self):
        """
        Return a dict that represents the tiers for a parent,
        ordered by descending start date.

        [{
            tier: USD TIER 1,
            start_date: 2012-09-01
        }]
        """
        return Parent.objects.filter(
            name=self.name,
            country=self.country
        ).order_by(
            '-start_date'
        ).values('tier', 'start_date')


class Retailer(models.Model):
    name = models.CharField(max_length=255)
    parent_name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
