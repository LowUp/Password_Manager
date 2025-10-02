# Password Manager
This password manager lets you store your passwords in a secure database. The database must be a MySQL database. You can use the password manager to generate strong passwords, encrypt, store, and retrieve them whenever you need.

## Features
The password manager has the following features:

- Stores your passwords in a secure database
- Generates strong passwords
- Allows you to retrieve your passwords when you need them
- Allows you to export your passwords in a CSV file
- Easy to use
## How to use
To use the password manager, follow these steps:

- Clone the project
- install requirements : ````pip install -r requirements.txt````
- Create a database and connect to it.
- Create a table to store your passwords (see 'table_structure.sql').
- Create a .env file and enter your DB info inside the file (see below).
``````
HOST=YOUR_HOST_NAME
BDD=YOUR_BDD_NAME
TABLE=YOUR_TABLE_NAME
USER=YOUR_BDD_USERNAME
PASSWORD=YOUR_BDD_PASSWORD
MASTER_KEY=ENTER_MASTER_KEY
``````
- Create a folder named ```logs``` at the root of the program
- Run the program : ````python3 password_container.py````
## Security
Before being stored in the DB, passwords are encrypted with a symmetric key automatically generated in a file named ```key.txt```.
## Conclusion
The password manager is a secure and easy-to-use tool that allows you to store your passwords in a safe place that you manage.
