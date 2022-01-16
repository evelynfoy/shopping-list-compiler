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
        recipe_title = recipes_list[index].name.replace("_", " ").title()
        print(f"{SPACES}{index + 1}) {recipe_title}")

def main():
    ''' This function runs the shopping list compiler application functions '''
    recipes_list = build_recipe_list()
    print("\n***  Welcome to the Shopping List Compiler Application.   ***\n")
    print(f"{SPACES}Here are the available recipes to order:\n")
    display_recipe_list(recipes_list)