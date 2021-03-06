from mailjet.connection import Connection
import json

class Api(object):
    def __init__(self, connection=None, access_key=None, secret_key=None):
        if not connection:
            connection = Connection.get_connection(access_key, secret_key)

        self.connection = connection

    def __getattr__(self, method):
        return ApiMethod(self, method)

class ApiMethod(object):
    def __init__(self, api, method):
        self.api = api
        self.method = method

    def __getattr__(self, function):
        return ApiMethodFunction(self, function)

    def __unicode__(self):
        return self.method

class ApiMethodFunction(object):
    def __init__(self, method, function):
        self.method = method
        self.function = function

    def __call__(self, **kwargs):
        response = self.method.api.connection.open(
            self.method,
            self.function,
            postdata=kwargs,
        )
        return json.load(response)

    def __unicode__(self):
        return self.function

