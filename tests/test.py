import unittest
from app import create_app, db
from app.models import User
from flask_testing import TestCase


class BasicTests(TestCase):

    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def test_login(self):
        resp = self.client.post('/auth/login', data={
            'username': 'user1',
            'password': 'test123'
        }, follow_redirects=True)
        self.assertIn(b'All assets', resp.data)

    def test_route(self):
        resp = self.client.get('/assets', follow_redirects=True)
        self.assertEqual(resp.status_code, 401)


if __name__ == '__main__':
    unittest.main()