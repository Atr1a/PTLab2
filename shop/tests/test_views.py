from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from shop.models import Product, Purchase
from datetime import date


class ViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user", password="12345")
        self.product = Product.objects.create(name="Table", price=100)

    def test_buy_redirects_if_not_auth(self):
        response = self.client.get(reverse("buy", args=[self.product.id]))
        self.assertEqual(response.status_code, 302)

    def test_buy_form_loads(self):
        self.client.login(username="user", password="12345")
        response = self.client.get(reverse("buy", args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

    def test_successful_purchase(self):
        self.client.login(username="user", password="12345")

        response = self.client.post(reverse("buy", args=[self.product.id]), {
            "address": "Moon Street",
        })

        self.assertEqual(response.status_code, 302)

        purchase = Purchase.objects.get(person=self.user)
        self.assertEqual(purchase.address, "Moon Street")
        self.assertEqual(purchase.price, self.product.price)

    def test_birthday_discount(self):
        self.user.profile.birthday = date.today()
        self.user.profile.save()

        self.client.login(username="user", password="12345")

        response = self.client.post(reverse("buy", args=[self.product.id]), {
            "address": "Discount Street",
        })

        purchase = Purchase.objects.latest("id")
        self.assertEqual(purchase.price, 90)
