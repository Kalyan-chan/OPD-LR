import unittest
from main import app

class quadratUr(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def post_request(self, a, b, c):
        return self.client.post('/', data=dict(a=str(a), b=str(b), c=str(c)))

    def test_1(self):
        response = self.post_request(1, 2, -8)
        self.assertIn('Два корня: x1 = 2.0, x2 = -4.0', response.data.decode('utf-8'))

    def test_2(self):
        response = self.post_request(1, -6, 9)
        self.assertIn('Один корень: x = 3.0', response.data.decode('utf-8'))

    def test_3(self):
        response = self.post_request(22, 11, 33)
        self.assertIn('Нет вещественных корней.', response.data.decode('utf-8'))

    def test_4(self):
        response = self.post_request(0, 2, 3)
        self.assertIn('Это не квадратное уравнение.', response.data.decode('utf-8'))

    def test_5(self):
        response = self.post_request('a', 'b', 'c')
        self.assertIn('Ошибка', response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()
