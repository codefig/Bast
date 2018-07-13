from tornado.web import RequestHandler
from tornado.web import HTTPError
import logging
from _json_ import Json as json_
from view import TemplateRendering
import os


class Controller(RequestHandler, TemplateRendering):

    def view(self, template_name, kwargs):
        """
        This is for making some extra context variables available to
        the template
        """
        # static_folder   = os.environ['STATIC_FOLDER']
        # template_folder = os.environ['TEMPLATE_FOLDER']
        # app_name        = os.environ['APP_NAME']

        kwargs.update({
            'settings': self.settings,
            'STATIC_URL': self.settings.get('static_url_prefix', '/static/'),
            'request': self.request,
            'xsrf_token': self.xsrf_token,
            'xsrf_form_html': self.xsrf_form_html,
        })
        content = self.render_template(template_name, kwargs)
        self.write(content)

    def data_received(self, chunk):
        pass

    def initialize(self, method):
        self.method = method

    def only(self, arguments):
        """
        returns the key, value pair of the arguments passed as a dict object
        Example usage
        data = self.only(['arg_name'])
        :param arguments:
        :return:
        """
        data = {}
        for i in arguments:
            data[i] = self.get_argument(i)
        return data

    def except_(self, arguments):
        """
        returns the arguments passed to the route except that set by user

        Example usage
        data = self.except_(['arg_name'])
        :param arguments:
        :return:
        """
        args = self.request.arguments
        data = {}
        for key, value in args.items():
            if key not in arguments:
                data[key] = self.get_argument(key)
        return data

    def json(self, data):
        """
        Encodes the dictionary being passed to JSON and sets the Header to application/json
        :param data:
        :return:
        """
        self.write(json_.encode(data))
        self.set_header('Content-type', 'application/json')

    def get(self, *args, **kwargs):
        try:
            func = getattr(self, self.method)
            if func:
                func()
            else:
                raise HTTPError(404)
        except AttributeError as e:
            logging.error(e.message)
            raise HTTPError(log_message="Controller Function not found")

    def post(self, *args, **kwargs):
        try:
            func = getattr(self, self.method)
            if func:
                func()
            else:
                raise HTTPError(404)
        except AttributeError as e:
            logging.error(e.message)
            raise HTTPError(log_message="Controller Function not found")
