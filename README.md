# On The Sales

#### Video Demo: <a target="_blank" href="https://youtu.be/LLb7Rdmefss">On The Sales - CS50 Final Project</a>

On The Sales is a responsive web application developed to make life easier for those who like to organize themselves when planning their sales.

The website organizes name, price, goals, planning dates, stock and small notes of your sale in cards filtered by _Selling_, _Not started_ and _Sold_, where each one represents a state of your sales.

<a href="https://imgur.com/tP3UDNr"><img src="https://i.imgur.com/tP3UDNr.gif" alt="Demonstration of On The Sales application" /></a>
First, you need to register an account. The application has some error messages if the user enters the wrong password confirmation and if the username already exists. As for the Log In part, there are also error messages if you enter the wrong password or if the account does not exist.

Then you add the sale you want to plan, filling in the required and optional fields, and it will appear on the main page. You can also delete your planning sale and account.

## What each file does?

- `static/` - contains the CSS and JavaScript file and the images used.

- `templates/` - contains all HTML pages.

- `onTheSales.db` - is the database created and used in the application, which was implemented with SQLite. Contains two tables:

  - **users**: contains the username, hashed password and user id of all accounts in the application.

  - **salesPlan**: the data of all planned sales.

- `app.py` - renders the entire application by Flask framework throught 7 functions:

  - `index()` - checks if there is a user and sends the planned sales data he made from the database to the **index.html** file.

  - `login()` - logs the user and creates a session for him.

  - `register()` - checks for errors, creates a hash password for the user and adds it to the database.

  - `plansale()` - plans the user's sale according to a certain filter, checks for possible typing errors (using the **isnumber()** function and others) and adds it to the sales database.

  - `delete()` - deletes a sale from database.

  - `account()` - deletes the user's account and all the sales he has planned, as well as disconnects him from the session and redirects to the main page.

  - `logout()` - disconnects from the session and redirects to **index.html** page.

- `requirements.txt` - contains all the libraries used for this application.

## Design choice

I made the initial design in Figma, but I ended up changing some things in the process, because I think it was more harmonious for the site.
You can view it <a target="_blank" href="https://www.figma.com/file/EfBaOIxMYA2G3I8xFviYkt/Final-Project?node-id=0%3A1&t=NOcaQXEuIFfbgn16-1">here</a> the initial design.

I chose a color palette with more green and brown tones because I believe it brings greater elegance without ceasing to be cozy for the user
