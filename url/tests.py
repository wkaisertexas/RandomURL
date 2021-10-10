import random

from django.test import TestCase

from .models import URL, Destination, User

NUMBER_OF_TRIALS = 10 ** 4
DECIMALS_CORRECT = 2


class URLTestCase(TestCase):
    def setUp(self):
        # Creates a base user to own everything (this was causing errors)
        self.sample_user = User.objects.create_user("sampleUser", "sample_user@gmail.com", "password123")

        # Creates a 50 / 50 Probability Distribution URL
        dest_a = Destination.objects.create(url='a', prob=0.5, views=0)
        dest_b = Destination.objects.create(url='b', prob=0.5, views=0)
        dest_a.save()
        dest_b.save()

        self.prob_a_and_b = URL.objects.create(owner=self.sample_user, link_string="hello_there")
        self.prob_a_and_b.destinations.add(dest_a, dest_b)

        # Sum not Equal to 100 Test
        dest_c = Destination.objects.create(url="c", prob=0.5, views=0)
        dest_c.save()

        self.prob_a_b_and_c = URL.objects.create(owner=self.sample_user, link_string="hello")
        self.prob_a_b_and_c.destinations.add(dest_a, dest_b, dest_c)

        # Saves all of the Objects
        self.prob_a_and_b.save()
        self.prob_a_b_and_c.save()

        # Ensures Reliability of Results
        random.seed(1)

    def test_get_destination_normal(self):
        """Tests the get_destination function under normal conditions. """

        percent_a = sum(
            [self.prob_a_and_b.get_destination() == 'a' for x in range(NUMBER_OF_TRIALS)]) / NUMBER_OF_TRIALS

        # self.assertTrue(0.5 + MARGIN_OF_ERROR > percent_a > 0.5 - MARGIN_OF_ERROR)  # Error less than one percent
        self.assertAlmostEqual(percent_a, 0.5, DECIMALS_CORRECT)

    def test_get_destination_error_resistant(self):
        percent_a = sum(
            [self.prob_a_b_and_c.get_destination() == 'a' for x in range(NUMBER_OF_TRIALS)]) / NUMBER_OF_TRIALS

        self.assertAlmostEqual(percent_a, 1 / 3, DECIMALS_CORRECT)

# TODO: Implement something that tests the creations of these tests cases from the web
