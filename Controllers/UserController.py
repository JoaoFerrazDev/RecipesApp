import datetime
from Models.User import User
from Controllers.BaseController import BaseHandler


class Register(BaseHandler):
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


class Login(BaseHandler):
    def get(self):
        self.render('Auth/Login.html')

    def post(self):
        email = self.get_argument('email')
        password = self.get_argument('password')
        session_token = User.login(email, password)
        if not session_token:
            self.redirect('/login')

        self.set_secure_cookie("session_token", session_token)
        self.redirect('/')


class Profile(BaseHandler):

    def get(self, id):
        user_info = User.get_user_profile(id)
        recipes = User.get_user_recipes(id)
        self.render('Account/Profile.html', user_info=user_info, recipes=recipes)

