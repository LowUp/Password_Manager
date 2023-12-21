import mysql.connector
from mysql.connector import Error
from dotenv import dotenv_values
import getpass
from password_classes import Query_manager

config = dotenv_values(".env")

def main():
    try:
        masterPass = getpass.getpass("Master password: \t")
        if masterPass != config['MASTER_KEY']:
            connection = None
            raise Exception("Access denied !")
        else :
            
            connection = mysql.connector.connect(host=config['HOST'],
                                                database=config['BDD'],
                                                user=config['USER'],
                                                password=config['PASSWORD'])
            
            bdd_connection = Query_manager(connection)   
            
            print("Welcome to your password manager !")

            while True:
                user_input = input(
                    "\n*****************************************\n\t1 - List services passwords\n\t2 - Add a password\n\t3 - Update a record\n\t4 - Delete a record\n\tAny other key - exit\n*****************************************\n")
                cursor = connection.cursor()
                if user_input == '1':
                    bdd_connection.display_all_passwords()
                    
                    passId = input("Choose password to reveal : \t")
                    bdd_connection.display_password(passId)

                elif user_input == '2':     
                    bdd_connection.add_password()

                elif user_input == '3':
                    bdd_connection.display_all_passwords()
                    
                    id_input = int(input("Which one do you want to update ? \t"))               
                    bdd_connection.edit_password(id_input)

                elif user_input == '4':
                    bdd_connection.display_all_passwords()
                    
                    id_input = int(input("Which record do you want to delete ? \t"))
                    bdd_connection.delete_password(id_input)

                else:
                    break

    except Error as e:
        print("Error while connecting to MySQL", e)
        
    finally:
        if connection != None:
            bdd_connection.close_connection()

if __name__ == '__main__':
    main()