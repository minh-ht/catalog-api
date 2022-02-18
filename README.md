# PROJECT CATALOG

GOT IT training program final project for backend intern. This application is a collection of APIs allow users to
register, login, create and view categories and items. This project is built with FastAPI framework, MySQL database and
SQLAlchemy.

## Prerequisites

These components are required for this application to work:

- Python 3.8 or later
- MySQL database 8.0.28 or later

## Set up virtual environment

<details>
  <summary>Click to expand!</summary>

To set up virtual environment, first you need to install virtualenv:

```
$ pip install virtualenv
```

To create and activate virtual environment, run this command in the terminal:

```
$ virtualenv venv --python=python3.8
$ source venv/bin/activate
```

</details>

## Installation

<details>
  <summary>Click to expand!</summary>

To install all the required libraries for this project, run this command:

`$ pip install -r requirements.txt`

</details>

## Setup environments

<details>
  <summary>Click to expand!</summary>

You might need to manually create MySQL databases for related environment: local, production and test (We may consider
setting up migration in the future). To create a database using MySQL, run this command in the terminal:

```
$ mysql -u <username> -p <password>
```

```mysql
mysql> create database <database_name>;
```

Create {environment}.env and fill in as .env.example

```
ENVIRONMENT="{environment}"

# Database config
SQL_ALCHEMY_DATABASE_URL="mysql+aiomysql://<username>:<password>@<host>:<port>/<database_name>"

# Security config
JWT_SECRET_KEY="***"
JWT_ALGORITHM="HS256"
JWT_EXPIRED_MINUTES=30
```

</details>

# Start the server

<details>
  <summary>Click to expand!</summary>

In the terminal, run this command:

```
$ python run.py
```

To start the server in different environment, run this command before running application in the terminal:

```
$ export ENVIRONMENT={environment}
```

as environment is your desired environment

</details>

# Testing

<details>
  <summary>Click to expand!</summary>

To run designed tests for this project, run these commands in the terminal:

```
$ export ENVIRONMENT="test"
$ pytest
```

</details>

_This project is licensed under the terms of the MIT license_
