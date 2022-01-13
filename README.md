<h1 >Shopping List Compiler</h1>

This is a Python command line application which runs in the Code Institute mock terminal on Heroku.

It is designed for use by a baking establishment but could be used by any business whose products are built from recipes or lists of ingredients/parts.

It compiles a complete list of ingredients and quantities required to fill the days orders.  

&nbsp;  

# How to use

The recipes or lists of ingredients are held on [Google Sheets]( https://en.wikipedia.org/wiki/Google_Sheets).  

The user is prompted to enter the days orders.

The complete list of required ingredients for all the orders are calculated.

The Shopping List is then displayed on the screen.

E.g. There are recipes provided for 3 different cakes
1. Lemon cake
2. Chocolate cake
3. Carrot cake

If the days orders are for 2 lemon, 3 chocolate and 1 carrot then the application will print out the complete list of ingredients and amounts required to make them.
e.g.
1. Flour - 2 Kg
2. Butter - 2 lb
etc

&nbsp; 

# Features

## Existing Features

- The application uses [Google Sheets]( https://en.wikipedia.org/wiki/Google_Sheets) to hold the data required.  
There is a single spreadsheet called recipes and each recipe has a sheet for its ingredients list where it holds the ingredient name and the quantity required.  

![recipes](docs/images/recipes.PNG)

- To access the spreadsheet the application uses 2 API's (Application Programming Interface).  
These are set up on the [Google Cloud Platform] (https://console.cloud.google.com/).
    - The first is Google Drive where it gets its credentials. These are stored in a json file called creds.json
    - The second is Google Sheets

- Input validation and error-checking
    - You can only enter positive integers values below 1000.  

- Data maintained in class instances  

- Responsive on all device sizes  


## Future Features

- Allow the addition, update, deletion and viewing of recipes
- Allow the addition, update, deletion and viewing of orders for a particular date
- Allow the addition, update, deletion and viewing of order levels for each ingredient

# Data Model

# Testing

# Bugs

## Solved Bugs

## Remaining Bugs

# Validator Testing

# Deployment

This project was deployed  using Code Institute's mock terminal for Heroku.

- Stes for deployment:
    - Fork or clone this repository 
    - Create a new Heroku app
    - Set up the buildbacks to <code>Python</code> and <code>NodeJS</code> in that order
    - Link the Heroku app to the repository
    - Click on <code>Deploy</code>


# Credits

* Code Institute for the deployment terminal
* [Simen Daehlin](https://github.com/Eventyret "Simen Daehlin") for code inspiration, help and advice.









