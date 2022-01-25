'''
Contains all the main functions for the application
'''

from datetime import date
import gspread
from google.oauth2.service_account import Credentials
import model


# Indents all lines displayed by an equal number of spaces
SPACES = "     "
WORKBOOK = None


def get_spreadsheet():
    '''
    Opens the spreadsheet and passes back a reference
    '''
    SCOPE = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
            ]
    CREDS = Credentials.from_service_account_file('creds.json')
    SCOPED_CREDS = CREDS.with_scopes(SCOPE)
    GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
    file = GSPREAD_CLIENT.open('recipes')
    return file


def get_spreadsheet_data(recipes, ingredients):
    '''
    Takes a list of recipes and a list of ingredient stock levels.
    Load data from Google spreadsheet into lists.
    Ignores shopping_list tab as that is not required.
    Returns updated lists
    '''
    print('\nPlease wait while the application information loads..........\n')
    global WORKBOOK
    WORKBOOK = get_spreadsheet()
    for sheet in WORKBOOK:
        if sheet.title == 'stock_levels':
            ingredients = build_ingredient_list(sheet)
        elif sheet.title != 'shopping_list':
            try:
                next_recipe = model.Recipe(sheet.title, sheet.get_all_values())
            except gspread.exceptions.SpreadsheetNotFound:
                print('Unfortunately we cannot access the recipes file right \
now. Please try again later')
            else:
                recipes.append(next_recipe)
    return [recipes, ingredients]


def build_ingredient_list(sheet):
    '''
    This function builds a list of ingredients from the stock levels sheet in
    Google Sheets.
    Each ingredient is held as an instance of the stock_levels class.
    This holds the ingredient name, unit, the current stock level and the
    re-order level.
    '''
    ingredients = []
    for ingredient in sheet.get_all_values():
        if ingredient[0] != 'Ingredient':
            next_ingredient = model.StockLevels(ingredient[0],
                                                ingredient[1],
                                                ingredient[2],
                                                ingredient[3])
            ingredients.append(next_ingredient)
    return ingredients


def display_recipe_list(recipes_list):
    '''
    This function reads through each recipe and prints it's name to the screen.
    It replaces the underscores in the recipe name with spaces and capitalises
    it.
    It takes a list of recipe objects and returns nothing
    '''
    for index in range(0, len(recipes_list)):
        recipe_title = recipes_list[index].format_recipe_name()
        print(f"{SPACES}{index + 1}) {recipe_title}")


def get_order(recipes_list, orders):
    '''
    This function gets an order from the screen and validates each element.
    The order comprises a recipe number and a quantity.
    It takes a list of objects and a dictionary of orders.
    If recipe exists in the order dictionary it increases the quantity of the
    order.
    If not it adds the recipe to the order.
    It returns the revised orders dictionary.
    '''
    # Get recipe number
    is_valid = False
    while not is_valid:
        try:
            recipe_number = int(input("\nPlease enter recipe number you wish \
to order:\n"))
            if recipe_number > 0 and recipe_number <= len(recipes_list):
                is_valid = True
            else:
                print("There is no recipe of that number in the list.")
        except ValueError:
            print('That was not a number.')

    # Get quantity
    is_valid = False
    while not is_valid:
        try:
            quantity = int(input("\nPlease enter the quantity you wish to \
order:\n"))
            if quantity > 0 and quantity < 10000:
                is_valid = True
            else:
                print("The quantity must be between 0 and 10,000.")
        except ValueError:
            print('That was not a number.')

    # Add order to order dictionary
    recipe = recipes_list[recipe_number-1]
    if recipe.name in orders:
        orders[recipe.name] += quantity
    else:
        orders[recipe.name] = int(quantity)
    print(f"\nYou have ordered {quantity} {recipe.format_recipe_name()}(s)")


def convert_to_stock_unit(recipe_unit, stock_level_unit, value):
    '''
    Takes the unit specified in the recipe, the unit specified in the stock
    levels and the value required
    Returns the value converted to kg from grams or litres from ml
    '''
    if (stock_level_unit == 'kg' and recipe_unit == 'g'):
        value /= 1000
    elif (stock_level_unit == 'l' and recipe_unit == 'ml'):
        value /= 1000
    return value


def compile_shopping_list(recipes, orders, stock_levels):
    '''
    Takes in a list of recipe objects, a dictionary of orders and a list of
    stock levels for each ingredient.
    Reads through the orders and calculates the quantities required for each
    order according to the ingredients and quantities specified in the recipes
    Returns a list of ingredients
    '''
    shopping_list = []
    for name in orders:
        recipe = next((recipe for recipe in recipes
                       if recipe.name == name), None)
        for ingredient in recipe.ingredients:
            stock_level = next((stock_level for stock_level
                                in stock_levels
                                if stock_level.name == ingredient.name
                                ), None)
            shopping_list_entry = next((ing for ing
                                        in shopping_list
                                        if ing.name == ingredient.name
                                        ), None)
            order_quantity = ingredient.quantity * orders[name]
            quantity_in_stock = (stock_level.convert_current_level() -
                                 stock_level.convert_reorder_level())
            if order_quantity > quantity_in_stock:
                stock_level.decrease_current_level(quantity_in_stock)
                addition_amt_required = order_quantity - quantity_in_stock
            else:
                stock_level.decrease_current_level(order_quantity)
                addition_amt_required = 0
            if addition_amt_required > 0:
                if stock_level.unit != ingredient.unit:
                    display_amt = convert_to_stock_unit(ingredient.unit,
                                                        stock_level.unit,
                                                        addition_amt_required)
                else:
                    display_amt = addition_amt_required
                if shopping_list_entry is None:
                    shopping_list.append(model.Ingredient(ingredient.name,
                                         display_amt,
                                         stock_level.unit))
                else:
                    shopping_list_entry.increase_quantity(
                        display_amt)
    return shopping_list


def display_orders(orders):
    '''
    Takes in a dictionary of orders
    Lists out the orders to the screen, writes them to a text file and to
    Google Sheets
    Returns nothing
    '''
    print("\nHere is the list of ingredients you will require to fill your \
order of:- \n")
    today = date.today().strftime("%d/%m/%Y")
    shopping_list_sheet = WORKBOOK.worksheet("shopping_list")
    with open('shopping_list.txt', 'w') as outfile:
        outfile.write(f"\nDate: {today}\n")
        outfile.write("\n*** Orders List ***\n")
        shopping_list_sheet.clear()
        shopping_list_sheet.append_row(['Date', 'Orders', 'Quantity'])
        for order in orders:
            print(f'{SPACES}{orders[order]} {order.replace("_", " ").title()} \
(s)')
            outfile.write(f'{SPACES}{orders[order]} \
{order.replace("_", " ").title()}(s)')
            outfile.write('\n')
            shopping_list_sheet.append_row([str(today),
                                            order.replace("_", " ").title() +
                                            '(s)', str(orders[order])])
        shopping_list_sheet.append_row([' ', '-------------------'])


def display_shopping_list(shopping_list):
    '''
    Takes in a list of ingredients
    Displays then on the screen, writes them to a text file and to Google
    Sheets
    Returns nothing
    '''
    sheet = WORKBOOK.worksheet("shopping_list")
    with open('shopping_list.txt', 'a') as outfile:
        outfile.write("\n*** Ingredients List ***\n")
        print("\n*** Ingredients List ***\n")
        sheet.append_row(['Item', 'Ingredients', 'Quantity', 'Unit'])
        for index in range(0, len(shopping_list)):
            item = shopping_list[index]
            print(f'{SPACES}{index + 1}) {item.name.title()} {item.quantity} \
{item.unit}')
            outfile.write(f'{SPACES}{index + 1}) {item.name.title()} \
{item.quantity} {item.unit}')
            outfile.write('\n')
            sheet.append_row([str(index + 1), item.name.title(),
                             str(item.quantity), item.unit])
        print("\n")
        sheet.append_row([' ', '-------------------'])


def main():
    '''
    This function runs the main application functions
    '''
    restart = 'y'
    while restart.lower() == 'y':
        try:
            recipes_list = []
            ingredients_list = []
            results = get_spreadsheet_data(recipes_list, ingredients_list)
            recipes_list = results[0]
            ingredients_list = results[1]
        except gspread.exceptions.SpreadsheetNotFound:
            print('Unfortunately we cannot access the recipes file right now.')
            print('Please try again later')
            restart = 'n'
        else:
            print("\n***  Welcome to the Shopping List Compiler Application.  \
 ***\n")
            orders = {}
            add_another_order = 'y'
            while add_another_order.lower() == 'y':
                print(f"{SPACES}Here are the available recipes to order:\n")
                display_recipe_list(recipes_list)
                get_order(recipes_list, orders)
                add_another_order = input("\nWould you like to enter another \
order (y/n)?\n")
                while add_another_order.lower() not in ('y', 'n'):
                    add_another_order = input("Would you like to enter another \
order (y/n)?\n")
            shopping_list = compile_shopping_list(recipes_list, orders,
                                                  ingredients_list)
            display_orders(orders)
            display_shopping_list(shopping_list)
            restart = input("\nWould you like to restart the application?\n")
            while restart.lower() not in ('y', 'n'):
                restart = input("Would you like to restart the application?\n")
    print("\n*** Goodbye. Thank you for using the Shopping List Compiler \
Application ***\n")
