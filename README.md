# Password Manager
This is a password manager that allows you to store your passwords in a secure database. The database must be a mysql database. You can use the password manager to generate strong passwords, store them, and retrieve them when you need them.

## Features
The password manager has the following features:

- Stores your passwords in a secure database
- Generates strong passwords
- Allows you to retrieve your passwords when you need them
- Easy to use
## How to use
To use the password manager, follow these steps:

- Clone the project
- install requirements : ````pip install -r requirements.txt````
- Create a database and connect to it.
- Create a table to store your passwords (see 'table_structure.sql').
- Create a .env file and enter your DB info inside the file 
``````
HOST=YOUR_HOST_NAME
BDD=YOUR_BDD_NAME
USER=YOUR_BDD_USERNAME
PASSWORD=YOUR_BDD_PASSWORD
MASTER_KEY=ENTER_MASTER_KEY
``````
- Run the program : ````python3 password_container.py````

## Conclusion
The password manager is a secure and easy-to-use tool that allows you to store your passwords in a safe place that is managed by you.
