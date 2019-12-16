from django.test import TestCase

# the most basic test...
class BasicTestCase(TestCase):
    def test_getting_root(self):
        self.client.get("/")
