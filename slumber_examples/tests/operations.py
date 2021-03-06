from mock import patch
from simplejson import loads

from django.test import TestCase

from slumber import Client
from slumber.connector.ua import post

from slumber_examples.models import Pizza
from slumber_examples.tests.configurations import ConfigureUser


class CreateTests(ConfigureUser, TestCase):
    def test_create_pizza(self):
        response, json = post('/slumber/slumber_examples/Pizza/create/', {
                'id': 1, 'name': 'Test P', 'for_sale': True})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Pizza.objects.all().count(), 1)

    def test_create_pizza(self):
        response1, json1 = post('/slumber/slumber_examples/Pizza/create/', {
                'id': 1, 'name': 'Test P', 'for_sale': True})
        self.assertEqual(response1.status_code, 200)
        response2, json2 = post('/slumber/slumber_examples/Pizza/create/', {
                'id': 1, 'name': 'Test P', 'for_sale': True})
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(Pizza.objects.all().count(), 1)


class OrderTests(ConfigureUser, TestCase):
    def setUp(self):
        super(OrderTests, self).setUp()
        self.pizza = Pizza(name='S1', for_sale=True)
        self.pizza.save()
        self.cnx = Client()

    def test_order_get(self):
        with patch('slumber.connector._get_slumber_authn_name', lambda: 'service'):
            pizza = self.cnx.slumber_examples.Pizza.get(id=self.pizza.id)
            self.assertEquals(pizza._operations['order'],
                'http://localhost:8000/slumber/slumber_examples/Pizza/order/1/')
            # Do an unsigned GET so there will be no user logged in
            response = self.client.get('/slumber/slumber_examples/Pizza/order/1/')
            self.assertEquals(response.status_code, 200, response.content)
            json = loads(response.content)
            self.assertEquals(json, dict(
                    _meta = dict(status=200, message="OK"),
                    form = dict(quantity='integer'),
                ))

    def test_order_post(self):
        pizza = self.cnx.slumber_examples.Pizza.get(id=self.pizza.id)
        response = self.client.post('/slumber/slumber_examples/Pizza/order/1/',
            dict(quantity=3))
        self.assertEquals(response.status_code, 501, response.content)

    def test_order_create_with_pk(self):
        pizza2 = self.cnx.slumber_examples.Pizza.create(id=2, name='S2', for_sale=True)
        pizza3 = Pizza.objects.create(name='S3', for_sale=True)
        self.assertEqual(Pizza.objects.count(), 3)
