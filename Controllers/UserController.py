import datetime
from Models.User import User
from Controllers.BaseController import BaseHandler
import os


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


class Logout(BaseHandler):
    def get(self):
        session_token = self.get_secure_cookie("session_token")

        if session_token:
            session_token = session_token.decode('utf-8')
            User.logout(session_token)

        self.redirect('/login')


class Profile(BaseHandler):

    def get(self, id):
        user_info = User.get_user_profile(id)
        recipes = User.get_user_recipes(id)
        self.render('Account/Profile.html', user_info=user_info, recipes=recipes)


class Edit(BaseHandler):
    def get(self, id):
        user = User.get_user_profile(id)
        print(user.image)
        if not user:
            self.write("User not found")
            self.redirect('/')
            return

        self.render('Account/Edit.html', user=user)

    def post(self, id):
        try:
            username = self.get_argument('username')
            email = self.get_argument('email')
            state = self.get_argument('state')
            password = self.get_argument('password')
            date_of_birth = self.get_argument('birth')

            # Handle image upload
            image_file = self.request.files.get('image', None)
            image_url = ''
            if image_file:
                # Save the uploaded image
                image_url = save_image(image_file[0])

            # Fetch the existing recipe
            user_data = User.get_user_profile(id)
            if not user_data:
                self.write("user not found")
                self.redirect('/')
                return

            # Create a Recipe object with the fetched data
            user = User(id, username=user_data.username, email=user_data.email, password=user_data.password,
                        date_of_birth=user_data.date_of_birth, state=user_data.state, image=user_data.image)

            # Update recipe details
            user.username = username
            user.state = state
            user.email = email
            user.date_of_birth = date_of_birth
            user.password = password
            # Update image URL if a new image is uploaded
            if image_url:
                user.image = image_url

            # Update the recipe in the database
            user.update(id)
            self.redirect(f'/profile/{id}')
        except ValueError as e:
            self.write(str(e))
            self.redirect(f'/edit-profile/{id}')


def save_image(image_file):
    try:
        upload_path = 'static/uploads'
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)

        image_filename = image_file['filename']
        image_path = os.path.join(upload_path, image_filename)

        # Save the image
        with open(image_path, 'wb') as f:
            f.write(image_file['body'])

        # Check if the file is written
        if os.path.exists(image_path):
            print(f"Image saved successfully: {image_path}")
        else:
            print(f"Failed to save image: {image_path}")

        # Return the relative URL of the saved image
        return f'/static/uploads/{image_filename}'
    except Exception as e:
        print(f"Error saving image: {str(e)}")
        return ''
