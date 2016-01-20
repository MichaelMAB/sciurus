import falcon
import json


class JSONTranslator(object):

    def process_response(self, req, resp, resource):

        resp.body = json.dumps(resp.body)


class Tester(object):

    def on_get(self, req, resp, **kwargs):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = {
            'quote': 'Two things awe me most, the starry sky '
                     'above me and the moral law within me.',
            'author': 'Immanuel Kant'
        }

    def on_post(self, req, resp, **kwargs):
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = {
            'result': 'You successfully submitted a POST request',
        }


api = falcon.API(middleware=[JSONTranslator()])

api.add_route('/test', Tester())
