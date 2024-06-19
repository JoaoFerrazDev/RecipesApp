import tornado.web
from Models.User import User


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_id = self.get_secure_cookie("session_token")
        if user_id:
            return user_id.decode("utf-8")
        return None

    def prepare(self):
        self.login = False
        self.current_user_id = -1
        if User.get_user_info(self.get_current_user()):
            self.current_user_id = User.get_user_info(self.get_current_user())['id']
            self.login = True

        self.template_variables = {
            "login": self.login,
            "current_user_id": self.current_user_id
        }

    def render(self, template_name, **kwargs):
        super().render(template_name, **{**self.template_variables, **kwargs})
