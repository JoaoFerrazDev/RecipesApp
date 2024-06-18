# models/recipe.py
from Services.DBContext import Database, _query


class Recipe:
    _observers = []

    def __init__(self, title, ingredients, instructions):
        self.title = title
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
        _query('INSERT INTO recipes (title, ingredients, instructions) VALUES (?, ?, ?)',
               (self.title, self.ingredients, self.instructions))

    @staticmethod
    def get_all_recipes():
        return _query('SELECT id, title, ingredients, instructions FROM recipes')

    @staticmethod
    def get_recipe_by_id(recipe_id):
        return _query('SELECT id, title, ingredients, instructions FROM recipes WHERE id = ?', (recipe_id,))

    @staticmethod
    def delete_recipe(recipe_id):
        return _query('DELETE FROM recipes WHERE id = ?', (recipe_id,))

    @staticmethod
    def get_recent_recipes():
        recipes = _query('SELECT id, title, ingredients, instructions FROM recipes ORDER BY id DESC LIMIT 6')
        return recipes


