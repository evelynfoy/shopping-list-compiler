'''
This file defines all classes for the Shopping List Compiler application.
'''

class Recipe:
    '''
    This class holds one recipe. The name, and a list of ingredients.
    Each ingredient is itself an object of class Ingredient
    '''
    def __init__(self, name, ingredients):
        self.name = name
        ingredients_list = []
        for ingredient in ingredients:
            if ingredient[0] != 'Ingredient':
                new_ingredient = Ingredient(ingredient[0], ingredient[1], ingredient[2])
                ingredients_list.append(new_ingredient)
        self.ingredients = ingredients_list

class Ingredient:
    '''
    This class holds one ingredient. The name, quantity and unit of item.
    '''
    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit
