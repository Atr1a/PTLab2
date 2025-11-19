from django.test import SimpleTestCase
from django.urls import resolve, reverse
from shop.views import buy_product


class URLsTest(SimpleTestCase):

    def test_buy_url(self):
        url = reverse("buy", args=[1])
        resolver = resolve(url)
        self.assertEqual(resolver.func, buy_product)
