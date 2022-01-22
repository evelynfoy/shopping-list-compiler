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
                new_ingredient = Ingredient(ingredient[0],
                                            ingredient[1],
                                            ingredient[2])
                ingredients_list.append(new_ingredient)
        self.ingredients = ingredients_list

    def format_recipe_name(self):
        '''
        Takes no prameters
        Returns the recipe title capitalized and with underscores from sheet
        name removed
        '''
        recipe_title = self.name.replace("_", " ").title()
        return recipe_title


class Ingredient:
    '''
    This class holds one ingredient. The name, quantity and unit of item.
    '''
    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    def increase_quantity(self, quantity):
        '''
        Takes a float value
        Reduces the instance quantity value bu the amount passed in
        Returns nothing
        '''
        self.quantity += quantity


class StockLevels(Ingredient):
    '''
    This class holds the stock levels for an ingredient.
    It also holds the stock unit which will likely be Kg rather than g for
    large quantities
    '''
    def __init__(self, name, unit, current_level, reorder_level):
        Ingredient.__init__(self, name, current_level, unit)
        self.reorder_level = float(reorder_level)

    def decrease_current_level(self, quantity):
        '''
        Takes the quantity to decrease the current level by
        Returns nothing
        '''
        if self.unit in ['kg', 'l']:
            self.quantity -= quantity/1000
        else:
            self.quantity -= quantity

    def convert_current_level(self):
        '''
        Takes no parameters
        Returns stock level of ingredient converted to grams or ml if held as
        kilograms or litres
        '''
        if self.unit in ['kg', 'l']:
            return self.quantity * 1000
        else:
            return self.quantity

    def convert_reorder_level(self):
        '''
        Takes no parameters
        Returns re-order level of ingredient converted to grams or ml if held
        as kilograms or litres
        '''
        if self.unit in ['kg', 'l']:
            return self.reorder_level * 1000
        else:
            return self.reorder_level
