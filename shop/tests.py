from django.test import TestCase
from django.urls import reverse
from .models import Category, Product, Order, OrderItem

class ShopModelTests(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name='Books', slug='books')
        self.prod = Product.objects.create(category=self.cat, name='Django 101', price=499.00, in_stock=True)

    def test_order_totals(self):
        order = Order.objects.create(customer_name='Alice', customer_email='alice@example.com')
        OrderItem.objects.create(order=order, product=self.prod, quantity=2, price_at_purchase=self.prod.price)
        self.assertEqual(order.total_items, 2)
        self.assertEqual(float(order.total_amount), 998.00)

class ViewsTests(TestCase):
    def test_healthcheck(self):
        url = reverse('healthcheck')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertJSONEqual(resp.content, {"status": "ok"})