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

    @classmethod
    def get_all_recipes(cls):
        cursor = cls.
        cursor.execute('SELECT id, title, ingredients, instructions FROM recipes')
        rows = cursor.fetchall()
        recipes = [cls(*row[1:]) for row in rows]
        return recipes

    @classmethod
    def get_recipe_by_id(cls, recipe_id):
        cursor = cls.dbContext.get_cursor()
        cursor.execute('SELECT id, title, ingredients, instructions FROM recipes WHERE id = ?', (recipe_id,))
        row = cursor.fetchone()
        if row:
            return cls(*row[1:])
        return None

    @classmethod
    def delete_recipe(cls, recipe_id):
        db = Database()
        cursor = db.get_cursor()
        cursor.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
        db.commit()
