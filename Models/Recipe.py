# models/recipe.py
from Services.DBContext import Database, _query


class Recipe:
    _observers = []

    def __init__(self, title, description, image, ingredients, instructions):
        self.title = title
        self.description = description
        self.image = image
        self.ingredients = ingredients
        self.instructions = instructions

    @classmethod
    def add_observer(cls, observer):
        cls._observers.append(observer)

    @classmethod
    def notify_observers(cls, recipe):
        for observer in cls._observers:
            observer.update(recipe)

    def save(self):
        query = f'''
            INSERT INTO recipes (title, description, image, ingredients, instructions)
            VALUES ('{self.title}', '{self.description}', '{self.image}', '{self.ingredients}', '{self.instructions}')
        '''
        _query(query)

    @staticmethod
    def get_all_recipes():
        query = 'SELECT id, title, description, image, ingredients, instructions FROM recipes'
        return _query(query)

    @staticmethod
    def get_recipe_by_id(recipe_id):
        query = f'SELECT id, title, description, image, ingredients, instructions FROM recipes WHERE id = {recipe_id}'
        return _query(query)

    @staticmethod
    def delete_recipe(recipe_id):
        query = f'DELETE FROM recipes WHERE id = {recipe_id}'
        return _query(query)

    @staticmethod
    def get_recent_recipes():
        query = 'SELECT id, title, description, image, ingredients, instructions FROM recipes ORDER BY id DESC LIMIT 6'
        return _query(query)
