
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

    lemon_cake = SHEET.worksheet('lemon_cake')

    data = lemon_cake.get_all_values()

    print(data)

def main():
    ''' This function runs the shopping list compiler application functions '''
    get_recipes()