from tornado.web import RequestHandler
from Models.User import User
from Controllers.BaseController import BaseHandler
from Services.Notifications import NotificationService


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
            print(user_id != self.template_variables["current_user_id"])
            if user_id != self.template_variables["current_user_id"]:
                User.follow_user(self.template_variables["current_user_id"], user_id)
                # Notify the followed user via a notification service
                notification_service = NotificationService()
                print(user_id)
                notification_service.notify_follow(user_id, self.template_variables["current_user_id"])

            self.redirect(f"/recipe/{recipe_id}")
        except ValueError as e:
            self.write(str(e))
            self.redirect('/')


class Unfollow(BaseHandler):
    def post(self):
        try:
            user_id = self.get_argument('user_id')
            recipe_id = self.get_argument('recipe_id')
            User.unfollow_user(self.template_variables["current_user_id"], user_id)
            # Notify the followed user via a notification service
            notification_service = NotificationService()
            notification_service.notify_unfollow(user_id, self.template_variables["current_user_id"])
            self.redirect(f"/recipe/{recipe_id}")
        except ValueError as e:
            self.write(str(e))
            self.redirect('/')


class Notifications(BaseHandler):
    def get(self):
        notification_service = NotificationService()
        notifications = notification_service.get_notifications(self.template_variables["current_user_id"])
        print(len(notifications))
        self.render('Account/Notifications.html', notifications=notifications)


class Followers(BaseHandler):
    def get(self):
        followers = User.get_user_followers(self.template_variables["current_user_id"])
        self.render('Account/Followers.html', followers=followers)


class Subscriptions(BaseHandler):
    def get(self):
        subscriptions = User.get_user_subscriptions(self.template_variables["current_user_id"])
        self.render('Account/Subscriptions.html', subscriptions=subscriptions)
