import mysql.connector
from mysql.connector import Error
from dotenv import dotenv_values
import getpass
from password_classes import Query_manager

config = dotenv_values(".env")

def search_loop(bdd_connection: object) -> None:
    while True:
        search_pass = input("\nSearch for a password ? (y/n): \t")
        search_pass = search_pass.lower()
        if search_pass == 'y':
            search = input("Type the service name : \t")
            bdd_connection.search_password(search)
        elif search_pass == 'n':
            break
        else:
            print("\nInvalid input !\n")
            
def export_options() -> bool:
    user_input = input("Decrypt passwords before export ? (y/n) : \t")
    user_input = user_input.lower()
    if user_input == 'y':
        return True
    elif user_input == 'n':
        return False
    else:
        print("\nAborted !")

# Main function

def main():
    try:
        masterPass = getpass.getpass("Master password: \t")
        if masterPass != config['MASTER_KEY']:
            connection = None
            raise Error("Access denied !")
        else :
            
            connection = mysql.connector.connect(host=config['HOST'],
                                                database=config['BDD'],
                                                user=config['USER'],
                                                password=config['PASSWORD'])
            
            bdd_connection = Query_manager(connection)   
            
            print("Welcome to your password manager !")

            while True:
                user_input = input(
                    "\n*****************************************\n\t1 - List services passwords\n\t2 - Add a password\n\t3 - Update a record\n\t4 - Delete a record\n\t5 - Export passwords to csv file\n\tAny other key - exit\n*****************************************\n")
                
                if user_input == '1':
                    bdd_connection.display_all_passwords()
                    
                    search_loop(bdd_connection)
                    
                    passId = input("Choose password to reveal : \t")
                    if passId != '':
                        bdd_connection.display_password(passId)
                    else:
                        print("\naborted")

                elif user_input == '2':     
                    bdd_connection.add_password()

                elif user_input == '3':
                    bdd_connection.display_all_passwords()
                    
                    search_loop(bdd_connection)
                    
                    id_input = input("Which one do you want to update ? \t") 
                    if id_input != '' and id_input.isdigit():        
                        bdd_connection.edit_password(int(id_input))
                    else:
                        print("\naborted")

                elif user_input == '4':
                    bdd_connection.display_all_passwords()
                    
                    search_loop(bdd_connection)
                    
                    id_input = input("Which record do you want to delete ? \t")
                    if id_input != '' and id_input.isdigit():
                        bdd_connection.delete_password(int(id_input))
                    else:
                        print("\naborted")
                
                elif user_input == '5':
                    bdd_connection.export_passwords(export_options())

                else:
                    break

    except Error as e:
        if str(e) == "Access denied !":
            print(e)
        else :
            print("Error while connecting to MySQL", e)
        
    finally:
        if connection != None:
            bdd_connection.close_connection()

if __name__ == '__main__':
    main()