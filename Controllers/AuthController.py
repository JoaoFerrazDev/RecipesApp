from tornado.web import RequestHandler
from Models.User import User


class AuthProxyHandler(RequestHandler):
    def initialize(self, real_handler_class):
        self.real_handler_class = real_handler_class

    def get(self):
        session_token = self.get_secure_cookie("session_token")
        print(f"Session Token: {session_token}")  # Debugging line to check the token

        if session_token:
            session_token = session_token.decode('utf-8')
            print(f"Decoded Session Token: {session_token}")  # Debugging line to check decoded token
            user = User.get_user_from_session(session_token)
            if user:
                real_handler = self.real_handler_class(self.application, self.request)
                real_handler._transforms = self._transforms
                real_handler.get()
                return

        self.redirect('/login')

    def post(self):
        real_handler = self.real_handler_class(self.application, self.request)
        real_handler._transforms = self._transforms
        real_handler.post()
