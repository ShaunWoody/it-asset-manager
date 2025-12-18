# Asset Manager application

A web application for managing asset collections. Users can browse assets and maintain their personal asset collection.
Admin users can manage the asset set and user accounts.

# Built With

- [Flask](https://flask.palletsprojects.com/) - Python web framework
- [Bootstrap 5](https://getbootstrap.com/) - CSS framework for UI styling
- [SQLite](https://www.sqlite.org/index.html) – SQL database used for data storage

# Getting Started

1. Create and activate virtual environment

python -m venv venv
venv\Scripts\activate

2. Install dependicies
pip install -r requirements.txt

3. Run the applcation
flask run

# Running Test

To run test after installing dependicies, run:

python -m app.tests.test

Make sure test are ran in venv

# Accounts for testing

Regular User - Username: user Password: test123
Admin User - Username: admin Password: test123

# Usage

- User registration and login

- Regular users can:
  - Browse all assets
  - Add assets to their collection
  - Edit their profile

- Admin users can:
  - Add, edit, or delete assets from the master asset list
  - View and manage all user accounts and their assets
  - Promote users to admin

# Acknowledgements

- Flask Documentation: https://flask.palletsprojects.com/
- Bootstrap 5: https://getbootstrap.com/
- Real Python - Flask Blueprints Guide: https://realpython.com/flask-blueprint/
- README structure: https://github.com/othneildrew/Best-README-Template

