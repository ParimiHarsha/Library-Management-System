Please follow the following steps to create and populate the database and run the web application

# Database Setup
 1. Install `MySQL` and `MySQLWorkbench` as instructed in the project guidelines.
 2. Create a new database and name it `LibraryManagementSystem`.
 3. In the `MySQLWorkbench` import the `creating_tables.sql` from sql_scripts folder and run it.
 4. After creating the table schemas, import the `inserting_data.sql` from the sql_scripts folder and run it.

At this point we should have a working database with proper table schemas and populated data tuples.

# Web Application Setup
1. Python Setup - Install the latest version of python 3.10 using your favourite installer\
2. Virtual Environment Setup
    - Install conda
    - Create new virtual environment using conda create --name venv python=3.10
    - Activate the conda environment using conda activate venv
    - Install `flask`, `mysql-connector-python` in that environment
3. Navigate to the current directory in the terminal and run `python app.py`

This should run the flask server locally and when we visit the localhost url we can play around with the web application.
