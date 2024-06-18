import datetime

from tornado.web import RequestHandler
from Models import User

class Register(RequestHandler):
    def get(self):
        self.render('Auth/Register.html')

    def post(self):
        try:
            username = self.get_argument('username')
            email = self.get_argument('email')
            password = self.get_argument('password')
            date_of_birth = self.get_argument('birth')
            User.register(username, email, password, date_of_birth)
            self.redirect('/login')
        except ValueError as e:
            self.write(str(e))
            self.redirect('/register')
class Login(RequestHandler):
    def get(self):
        self.render('Auth/Login.html')

    def post(self):
        email = self.get_argument('email')
        password = self.get_argument('password')
        User.login(email, password)

        self.redirect('/')