import main
import unittest
import json
import flask

jsonify = main.jsonify

def get_api_json_data(response):
    if not type(response) == flask.Response:
        print('response must be a flask.Response object')
        return
    with main.app.app_context():
        try:
            return json.loads(response.get_data(as_text=True))
        except:
            print('response must be jsonifiable, such as an api endpoint')

def get_route_status_code(response):
    if not type(response) == flask.Response:
        print('response must be a flask.Response object')
        return
    with main.app.app_context():
        return response.status_code 


'''
class routeTestExample(unittest.TestCase):

    def setUp(self):
        main.app.testing = True
        self.app = main.app.test_client()
    
    def test_route_or_api_endpoint_example(self):
        res = self.app.get('/routeName')
        print(get_api_json_data(res))
        print(get_route_status_code(res))

    def tearDown(self):
        pass
'''

if __name__ == '__main__':
    unittest.main()