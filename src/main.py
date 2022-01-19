import model

# Indents all lines displayed by an equal number of spaces
SPACES = "     "

def build_recipe_list():
    ''' 
    This function builds a list of recipes from the spreadsheet in Google Sheets.
    Each recipe is held as an instance of the recipe class.
    This holds the recipe name and list of ingredients and quantity .
    The class recipe 
    '''
    RECIPES_SHEET = get_recipes()
    worksheet_list = RECIPES_SHEET.worksheets()
    recipes = []
    for recipe in RECIPES_SHEET:
        new_recipe = model.Recipe(recipe.title, recipe.get_all_values())
        recipes.append(new_recipe)
    return(recipes)    

def get_recipes():
    ''' Read recipes in for recipes spreadsheet on Google Sheets''' 
    import gspread
    from google.oauth2.service_account import Credentials

    SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
        ]

    CREDS = Credentials.from_service_account_file('creds.json')
    SCOPED_CREDS = CREDS.with_scopes(SCOPE)
    GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
    SHEET = GSPREAD_CLIENT.open('recipes')
    return SHEET

def display_recipe_list(recipes_list):
    ''' 
    This function reads through each recipe and prints it to the screen.
    It replaces the underscores in the recipe name with spaces and capitalises 
    it.
    '''
    for index in range(0, len(recipes_list)):
        recipe_title = recipes_list[index].format_recipe_name()
        print(f"{SPACES}{index + 1}) {recipe_title}")

def get_order(recipes_list, orders):
    ''' This function gets an order from the screen.'''
    # Get recipe number
    is_valid = False
    while not is_valid:
        try:
            recipe_number = int(input("\nPlease enter recipe number you wish to order:\n"))
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
            quantity = int(input("\nPlease enter the quantity you wish to order:\n"))
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
        orders[recipe.name] = quantity
    print(f"\nYou have ordered {quantity} {recipe.format_recipe_name()}(s)")

def get_recipe(recipes, name):
    ''' 
    Takes in a list of recipe objects and a string. 
    Loops through the list of recipe objects until one matches the name
    passed in.
    Returns a recipe object
    '''
    found = False
    index = 0
    while not found and index < len(recipes):
        if recipes[index].name == name:
            found = True
        else:
            index += 1
    return recipes[index]

def get_ingredient(ingredients, name):
    '''
    Takes in a list of ingredient objects and a string.
    Loops through the list of ingredient objects until one matches the name
    passed in
    Returns an ingredients object
    '''
    found = False
    index = 0
    while not found and index < len(ingredients):
        if ingredients[index].name == name:
            found = True
        else:
            index += 1
    if not found:
        return None
    else:
        return ingredients[index]

def compile_shopping_list(recipes, orders):
    ''' 
    Takes in a list of recipe objects and a dictionary of orders.
    Reads through the orders and calculates the quantities required for each order
    according to the ingredients and quantities specified in the recipes
    Returns a list of ingredients
    '''
    shopping_list = []
    for name in orders:
        recipe = get_recipe(recipes, name)
        for ingredient in recipe.ingredients:
            current_ingredient = get_ingredient(shopping_list, ingredient.name)
            order_quantity = float(ingredient.quantity) * float(orders[name])
            if current_ingredient is None:
                shopping_list.append(model.Ingredient(ingredient.name, order_quantity, ingredient.unit))
            else:
                current_ingredient.increase_quantity(order_quantity)
    return shopping_list

def display_orders(orders):
    ''' 
    Takes in a dictionary of orders
    Lists out the orders to the screen
    Returns nothing
    '''
    print("\nHere is the list of ingredients you will require to fill your order of:- \n")
    for order in orders:
        print(f'{SPACES}{orders[order]} {order.replace("_", " ").title()}(s)')

def display_shopping_list(shopping_list):
    ''' 
    Takes in a list of ingredients
    Displays then on the screen
    Returns nothing
    '''
    print("\n*** Ingredients List ***\n")
    for index in range(0, len(shopping_list)):
        print(f'{SPACES}{index + 1}) {shopping_list[index].name.title()} {shopping_list[index].quantity} {shopping_list[index].unit}')
    print("\n")

def main():
    ''' 
    This function runs the shopping list compiler application functions 
    '''
    try:
        recipes_list = build_recipe_list()
    except:
        print('Unfortunately we cannot access the recipes file right now. Please try again later')
    else:
        add_another_order = 'y'
        while add_another_order.lower() == 'y':
            print("\n***  Welcome to the Shopping List Compiler Application.   ***\n")
            orders = {}
            add_another_order = 'y'
            while add_another_order.lower() == 'y':
                print(f"{SPACES}Here are the available recipes to order:\n")
                display_recipe_list(recipes_list)
                get_order(recipes_list, orders)
                add_another_order = input("\nWould you like to enter another order (y/n)?\n")
                while add_another_order.lower() not in ('y','n'): 
                    add_another_order = input("Would you like to enter another order (y/n)?\n")
            shopping_list = compile_shopping_list(recipes_list, orders)
            display_orders(orders)
            display_shopping_list(shopping_list)
            add_another_order = input("\nWould you like to enter another order (y/n)?\n")
            while add_another_order.lower() not in ('y', 'n'): 
                add_another_order = input("Would you like to enter another order (y/n)?\n")
    
