from tornado.web import RequestHandler
from Models.User import User


class Create(RequestHandler):
    def get(self):
        self.render('Recipes/Create.html')

    def post(self):
        try:
            username = self.get_argument('username')
            email = self.get_argument('email')
            password = self.get_argument('password')
            date_of_birth = self.get_argument('birth')
            user = User.register(username, email, password, date_of_birth)
            session_token = User.create_session(user)
            self.set_secure_cookie("session_token", session_token)
            self.redirect('/login')
        except ValueError as e:
            self.write(str(e))
            self.redirect('/create')
