from tornado.web import RequestHandler
from Models.User import User
from Controllers.BaseController import BaseHandler


class Recipes(BaseHandler):
    def get(self):
        session_token = self.get_secure_cookie("session_token")

        if session_token:
            session_token = session_token.decode('utf-8')
            user_info = User.get_user_info(session_token)
            recipes = User.get_user_recipes(user_info['id'])
            self.render('Recipes/Index.html', recipes=recipes)


class Follow(BaseHandler):
    def post(self):
        try:
            user_id = self.get_argument('user_id')
            recipe_id = self.get_argument('recipe_id')
            print(user_id is not self.template_variables["current_user_id"])
            if user_id is not self.template_variables["current_user_id"]:
                User.follow_user(self.template_variables["current_user_id"], user_id)
            self.redirect(f"/recipe/{recipe_id}")
        except ValueError as e:
            self.write(str(e))
            self.redirect('/')

class Notifications(RequestHandler):
    def get(self):
        notifications = User.get_user_info().notifications.all()
        self.render('Account/Notifications.html', notifications=notifications)


class Followers(RequestHandler):
    def get(self):
        followers = User.get_user_info().followers.all()
        self.render('Account/Followers.html', followers=followers)


class Subscriptions(RequestHandler):
    def get(self):
        subscriptions = User.get_user_info().subscriptions.all()
        self.render('Account/Subscriptions.html', subscriptions=subscriptions)
