import unittest
import json
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_create_order_valid(self):
        # Test creating an order with valid components
        data = {"components": ["I", "A", "D", "F", "K"]}
        response = self.app.post('/orders', json=data)
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 201)
        self.assertTrue(data.get('order_id'))
        self.assertTrue(data.get('total') > 0)
        self.assertTrue(data.get('parts'))
    
    def test_create_order_invalid_combination(self):
        # Test creating an order with invalid combination of components
        data = {"components": ["I", "A", "D", "F"]}
        response = self.app.post('/orders', json=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid combination of components', response.data)

    def test_create_order_missing_components(self):
        # Test creating an order with missing components
        data = {}
        response = self.app.post('/orders', json=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid request format', response.data)

if __name__ == '__main__':
    unittest.main()
