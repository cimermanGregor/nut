import json
import requests


class APIClient():
    """
    API Client class for connecting to REST api and running requests gainst it.
    """

    def __init__(self,
                 api_url='http://0.0.0.0:8000',
                 api_path='api/v1',
                 api_token="token"):

        self.url = "%s/%s" % (api_url, api_path)
        self.auth = {'Authorization': "%s %s" % ('Token', api_token)}
        schema = requests.get(
            self.url,
            headers=self.auth,
        )
        self.schema = schema.json()

    def get(self, path):
        response = requests.get(path, headers=self.auth)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Response not expected. Details: %s" %
                            response.json())

    def post(self, path, payload):
        response = requests.post(path, headers=self.auth, data=payload)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise Exception("Response not expected. Details: %s" %
                            response.json())

    def put(self, path, payload):
        response = requests.put(path, headers=self.auth, data=payload)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise Exception("Response not expected. Details: %s" %
                            response.json())

    def patch(self, path, payload):
        response = requests.patch(path, headers=self.auth, data=payload)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            print response.status_code
            raise Exception("Response not expected. Details: %s" %
                            response.json())

    def delete(self, path):
        response = requests.delete(path, headers=self.auth)
        if response.status_code in [200, 204]:
            return True
        else:
            print response.status_code
            raise Exception("Response not expected. Details: %s" %
                            response.json())
