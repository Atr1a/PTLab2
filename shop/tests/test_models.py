from django.test import TestCase
from django.contrib.auth.models import User
from shop.models import Profile, Product, Purchase
from decimal import Decimal


class ModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="atria",
            password="12345",
            email="a@a.com"
        )
        self.profile = Profile.objects.get(user=self.user)
        self.profile.birthday = "2000-05-05"
        self.profile.save()

        self.product = Product.objects.create(
            name="Test Product",
            price=Decimal("199.99")
        )

    def test_profile_str(self):
        self.assertEqual(str(self.profile), "atria")

    def test_product_str(self):
        self.assertEqual(str(self.product), "Test Product")

    def test_purchase_str(self):
        purchase = Purchase.objects.create(
            person=self.user,
            address="Somewhere",
            product=self.product,
            price=self.product.price
        )
        self.assertEqual(str(purchase), "atria — Test Product")

    def test_profile_birthday_saved(self):
        self.assertEqual(str(self.profile.birthday), "2000-05-05")

    def test_product_price_decimal(self):
        self.assertIsInstance(self.product.price, Decimal)

    def test_purchase_relations(self):
        purchase = Purchase.objects.create(
            person=self.user,
            address="City",
            product=self.product,
            price=self.product.price
        )

        self.assertEqual(purchase.person.username, "atria")
        self.assertEqual(purchase.product.name, "Test Product")
        self.assertEqual(purchase.price, Decimal("199.99"))
