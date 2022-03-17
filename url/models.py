import string
from random import random, choice

from django.contrib.auth.models import AbstractUser
from django.db import models

LINK_STRING_LENGTH = 8

class User(AbstractUser):
    pass


class Destination(models.Model):
    views = models.IntegerField(default=0)
    prob = models.DecimalField(max_digits=6, decimal_places=4)
    url = models.URLField()

    def __str__(self):
        return f"{self.url} with a {self.prob * 100:.0f}% chance"

    def pp_prob(self):
        return f"{self.prob * 100:.0f} %"

    def get_value(self):
        """Gets the value for each slider in the edit view"""
        return int(self.prob * 100)


class URL(models.Model):
    title = models.CharField(max_length=50)
    link_string = models.CharField(max_length=10)
    destinations = models.ManyToManyField(Destination, related_name="url_group")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="urls")

    def __str__(self):
        return f"URL with {self.destinations.count()} destinations"

    def get_destination(self):
        """Randomly picks a destination"""
        rand = random() * self.get_cum_probability()
        for dest in self.destinations.all():
            rand -= float(dest.prob)
            if rand <= 0:
                dest.views += 1
                dest.save()
                return dest.url
        dest = self.destinations.last()
        dest.views += 1
        dest.save()
        return dest  # This should never be run in theory

    def get_cum_probability(self):
        """Gets the sum of all individual probabilities (should equal 1)"""
        return float(sum([dest.prob for dest in self.destinations.all()]))

    def get_max_probability(self):
        """Gets the maximum of all of the probabilities (scales the items)"""
        return float(max([dest.prob for dest in self.destinations.all()]))

    def get_views(self):
        """Counts the total number of views present on a link (this code is most definitely slower, but golf)"""
        return sum([dest.views for dest in self.destinations.all()])

    def set_link_string(self):
        char_set = string.ascii_letters + string.digits  # + string.punctuation
        self.link_string = ''.join(choice(char_set) for i in range(LINK_STRING_LENGTH))  # Makes random 10 digit string

