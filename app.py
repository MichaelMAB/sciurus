import falcon
import json
from json import JSONEncoder
from pymongo import MongoClient
import os
from config import configs

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]


class MongoEncoder(JSONEncoder):

    def default(self, obj, **kwargs):
        from bson import ObjectId
        if isinstance(obj, ObjectId):
            return str(obj)
        else:
            return JSONEncoder.default(obj, **kwargs)


class JSONTranslator(object):

    def process_request(self, req, resp):
        # req.stream corresponds to the WSGI wsgi.input environ variable,
        # and allows you to read bytes from the request body.
        #
        # See also: PEP 3333
        if req.content_length in (None, 0):
            # Nothing to do
            return
        content_type = req.get_header('Content-Type')
        if content_type == "application/json":
            body = req.stream.read()
            if not body:
                raise falcon.HTTPBadRequest(
                    'Empty request body',
                    'A valid JSON document is required.')

            try:
                req.context['doc'] = json.loads(
                    body.decode('utf-8'))

            except (ValueError, UnicodeDecodeError):
                raise falcon.HTTPError(
                    falcon.HTTP_753,
                    'Malformed JSON',
                    'Could not decode the request body. The '
                    'JSON was incorrect or not encoded as '
                    'UTF-8.')

    def process_response(self, req, resp, resource):
        if not resp.body:
            return

        resp.body = json.dumps(resp.body, cls=MongoEncoder)


class Sciurus(object):

    def __init__(self, db=None):
        if not db:
            raise ValueError("You must provide a db")
        self.items = db.test

    def on_get(self, req, resp, **kwargs):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        cursor = self.items.find()
        items = []
        for item in cursor:
            items.append(item)
        resp.body = items

    def on_post(self, req, resp, **kwargs):
        obj = req.context['doc']
        result = self.items.insert_one(obj)
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = {
            'result': 'You did it. Here is the id:{0}'.format(result),
        }

api = falcon.API(middleware=[JSONTranslator()])

app_config = configs[os.getenv('CONFIG', 'default')]

client = MongoClient(host=app_config.HOST)
db = client[app_config.DB]

api.add_route('/test', Sciurus(db))

print "Running App"
