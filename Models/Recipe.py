# models/recipe.py
from Services.DBContext import Database


class Recipe:
    _observers = []

    def __init__(self, title, ingredients, instructions):
        self.title = title
        self.ingredients = ingredients
        self.instructions = instructions
        self.dbContext = Database()

    @classmethod
    def add_observer(cls, observer):
        cls._observers.append(observer)

    @classmethod
    def notify_observers(cls, recipe):
        for observer in cls._observers:
            observer.update(recipe)

    def save(self):
        cursor = self.dbContext.get_cursor()
        cursor.execute('INSERT INTO recipes (title, ingredients, instructions) VALUES (?, ?, ?)', (self.title, self.ingredients, self.instructions))
        self.dbContext.commit()
        self.notify_observers(self)

    def get_all_recipes(self):
        cursor = self.dbContext.get_cursor()
        cursor.execute('SELECT id, title, ingredients, instructions FROM recipes')
        rows = cursor.fetchall()
        return recipes

    def get_recipe_by_id(self, recipe_id):
        cursor = self.dbContext.get_cursor()
        cursor.execute('SELECT id, title, ingredients, instructions FROM recipes WHERE id = ?', (recipe_id,))
        row = cursor.fetchone()
        return None

    def delete_recipe(self, recipe_id):
        cursor = self.dbContext.get_cursor()
        cursor.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
        self.dbContext.commit()
