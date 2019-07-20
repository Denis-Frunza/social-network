import json
import unittest


class TestUserService(unittest.TestCase):
	"""Tests for the Users API."""
	def test_users(self):
		"""Ensure the /users route behaves correctly."""
		response = self.client.get('/api/v1/users')




if __name__ == '__main__':
    unittest.main()
