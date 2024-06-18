from Models.User import User
from tornado.web import RequestHandler


class AuthProxyHandler(RequestHandler):
    def initialize(self, real_handler):
        self.real_handler = real_handler

    def get(self):
        session_token = self.get_secure_cookie("session_token")
        if session_token and User.get_user_from_session(session_token.decode('utf-8')):
            self.real_handler.get()
        else:
            self.redirect('/')

    def post(self):
        self.real_handler.post()
