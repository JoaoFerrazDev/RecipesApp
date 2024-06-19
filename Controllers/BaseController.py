import tornado.web
from Models.User import User


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        session_token = self.get_secure_cookie("session_token")
        if session_token:
            return session_token.decode("utf-8")
        return None

    def prepare(self):
        self.login = False
        self.current_user_id = None
        current_user = self.get_current_user()

        if current_user:
            user_info = User.get_user_info(current_user)
            if user_info:
                self.current_user_id = user_info['id']
                self.login = True

        self.template_variables = {
            "login": self.login,
            "current_user_id": self.current_user_id
        }

    def render(self, template_name, **kwargs):
        super().render(template_name, **{**self.template_variables, **kwargs})
