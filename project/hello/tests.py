from django.test import Client, TestCase

class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_html_pass(self):
        # Issue a GET request.
        response = self.client.get('/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.content, b'<p>Hello, World</p>')

    def test_json_pass(self):
        # Issue a GET request.
        response = self.client.get('/', HTTP_ACCEPT='application/json')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.content, b'{"message": "Hello, World"}')
