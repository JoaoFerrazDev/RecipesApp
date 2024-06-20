# Controllers/AuthProxyHandler.py

from Controllers.BaseController import BaseHandler
from Models.User import User


class AuthProxyHandler(BaseHandler):
    def initialize(self, real_handler_class):
        self.real_handler_class = real_handler_class

    def prepare(self):
        super().prepare()
        self.session_token = self.get_secure_cookie("session_token")
        self.user = None

        if self.session_token:
            self.session_token = self.session_token.decode('utf-8')
            self.user = User.get_user_from_session(self.session_token)

        if not self.user:
            self.redirect('/login')
            return

    def delegate_request(self):
        real_handler = self.real_handler_class(self.application, self.request)
        real_handler._transforms = self._transforms
        real_handler.current_user = self.user
        real_handler.template_variables = self.template_variables
        real_handler.prepare = self.prepare  # Pass the prepare method
        return real_handler

    def get(self, argument=None):
        if self.user:
            real_handler = self.delegate_request()
            if argument is None:
                real_handler.get()
            else:
                real_handler.get(argument)
        else:
            self.redirect('/login')

    def post(self, argument=None):
        if self.user:
            real_handler = self.delegate_request()
            if argument is None:
                real_handler.post()
            else:
                real_handler.post(argument)
        else:
            self.redirect('/login')
