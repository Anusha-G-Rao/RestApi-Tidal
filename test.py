import unittest

try:
    from app.app import app

except Exception as e:
    print("Some Modules are Missing {}".format(e))


class FlaskTest(unittest.TestCase):
    LOGIN_URL = "http://127.0.0.1:8080/login"

    data = {
        "email": "testfail@bridge.de",
        "password": "whyinplaintext"
    }

    # check for response 200
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # check id content return is application /json
    def test_index_content(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertEqual(response.content_type, "application/json")

    # check /stats route
    def test_stats_route(self):
        tester = app.test_client(self)
        response = tester.get("/stats")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # check for Data returned
    def test_index_data(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertTrue(b'arrived' in response.data)

    # check for login url
    def test_login(self):
        tester = app.test_client(self)
        response = tester.post(self.LOGIN_URL, json=self.data)
        statuscode = response.status_code
        self.assertEqual(statuscode, 401)


if __name__ == "__main__":
    unittest.main()
