from Models.Recipe import Recipe
from Models.User import User
import os
from PIL import Image
from Controllers.BaseController import BaseHandler


class Create(BaseHandler):
    def get(self):
        self.render(template_name='Recipes/Create.html')

    def post(self):
        try:
            title = self.get_argument('title')
            description = self.get_argument('description')
            ingredients = self.get_argument('ingredients')
            instructions = self.get_argument('instructions')

            # Handle image upload
            print("Received files: ", self.request.files)
            image_file = self.request.files.get('image', None)
            image_url = ''
            if image_file:
                # Save the uploaded image
                image_url = self.save_image(image_file[0])

            recipe = Recipe(title, description, image_url, ingredients, instructions)
            recipe.save(self.template_variables["current_user_id"])
            self.redirect('/')
        except ValueError as e:
            self.write(str(e))
            self.redirect('/create-recipe')

    def save_image(self, image_file):
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


class RecipePage(BaseHandler):
    def get(self, id):
        print("recipe")
        recipe = Recipe.get_recipe_by_id(id)
        print(f"Debug: Query Result for recipe_id {id} -> {recipe[0]}")
        self.render('Recipe/Index.html', recipe=recipe)

