# from user_cred.app import index
import unittest
import requests


class TestAPI(unittest.TestCase):
    URL = 'http://localhost:5000/users'

    data = {"name": "unit testing", "email": "Testing@gmail.com"}
    expected_result = {
        "email": "harikesh.porter@example.com",
        "id": 23,
        "username": "harikesh porter",
    }



    def test2_create_users(self):
        resp = requests.get(self.URL)
        self.assertEqual(resp.status_code, 200)
        print("Test 2 completed")

    def test3_get_specific_user(self):
        resp = requests.get(self.URL + "/3")
        self.assertEqual(resp.status_code, 200)
        print("Test 3 completed")

    def test4_delete_record(self):
        resp = requests.get(self.URL + "/2")
        self.assertEqual(resp.status_code, 200)
        print("Test 4 completed")


if __name__ == "__main__":
    unittest.main()
