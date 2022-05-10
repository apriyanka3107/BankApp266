SWE266P: Online Banking App
======

**A self-contained web app for online banking with 4 vulnerabilities.**

### Requirements
- Python 3.7

### Frontend
- HTML
- CSS

### Backend
- Python
- SQLite3
- Flask

 Installation: Mac
-------

### Clone The Repository

    # Clone the repository.
    $ git clone https://github.com/apriyanka3107/BankApp266.git

### Create and Activate a Virtual Environment
    # Go to the project directory.
    $ cd BankApp266

    # Create an environment.
    $ python3 -m venv venv

    # Activate the environment.
    $ . venv/bin/activate

### Install Dependencies
    # Ensure Flask is installed.
    $ pip install flask

    # Ensure all dependencies are installed.
    $ pip install -e .
Run: Mac
---

### Ensure you are in correct directory
    $ cd src

### Tell Flask where to find the application and how to run it
    # Tell Flask where the app is located.
    $ export FLASK_APP='Bank266p'
    
    # Run the app in 'production' mode.
    $ export FLASK_ENV='production'

### Initialize the database
    # Initialize the database.
    $ flask init-db

### Run the application
    # Run the application.
    $ flask run

Open http://127.0.0.1:5000 in a browser.

Installation: Windows
-------

### Clone The Repository
    # clone the repository
    $ git clone https://github.com/apriyanka3107/BankApp266.git

### Create and Activate a Virtual Environment
    # Go to the project directory.
    $ cd BankApp266

    # Create an environment.
    $ python3 -m venv venv

    # Activate the environment.
    $ . venv\Scripts\activate

### Install Dependencies
    # Ensure Flask is installed.
    $ pip install flask

    # Ensure all dependencies are installed.
    $ pip install -e .

Run: Windows
---

### Ensure you are in correct directory
    $ cd src
    
### Tell Flask where to find the application and how to run it
    # Tell Flask where the app is located.
    $ set FLASK_APP='Bank266p'

    # Run the app in 'production' mode.
    $ set FLASK_ENV='production'

### Initialize the database
    $ flask init-db

### Run the application
    $ flask run

Open http://127.0.0.1:5000 in a browser.


