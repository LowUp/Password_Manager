import mysql.connector
from mysql.connector import Error
from dotenv import dotenv_values
import getpass

config = dotenv_values(".env")


try:
    masterPass = getpass.getpass("Master password: \t")
    if masterPass != config['MASTER_KEY']:
        raise Exception("Access denied !")
    else :
        connection = mysql.connector.connect(host=config['HOST'],
                                            database=config['BDD'],
                                            user=config['USER'],
                                            password=config['PASSWORD'])
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)

            while True:
                user_input = input(
                    "\n*****************************************\n\t1 - List services passwords\n\t2 - Add a password\n\t3 - Update a record\n\t4 - Delete a record\n\tAny other key - exit\n*****************************************\n")
                cursor = connection.cursor()
                if user_input == '1':
                    cursor.execute("select * from passwords;")
                    record = cursor.fetchall()
                    print("| id | - | service |")
                    for count, value in enumerate(record):
                        print(
                            f"| {value[0]} | - | {value[1]} |\n")
                    
                    passId = input("Choose password to reveal : \t")
                    for count, value in enumerate(record):
                        if value[0] == int(passId):
                            print("| id | - | service | - | username | - | password |\n")
                            print(
                            f"| {value[0]} | - | {value[1]} | - | {value[2]} | - | {value[3]} |\n")
                            break


                elif user_input == '2':
                    service = input("Input service name : \t")
                    identifiant = input("Input username : \t")
                    mdp = input("Type your password : \t")
                    cursor.execute(
                        f"insert into passwords (service, identifiant, mdp) values ('{service}', '{identifiant}', '{mdp}');")
                    connection.commit()
                    print(cursor.rowcount,
                        "Data inserted !")
                    cursor.close()

                elif user_input == '3':
                    input_dict = {}
                    
                    cursor.execute("select * from passwords;")
                    record = cursor.fetchall()
                    
                    print("| id | - | service |")
                    
                    for count, value in enumerate(record):
                        print(
                            f"| {value[0]} | - | {value[1]} |\n")
                    
                    id_input = int(input("Which one do you want to update ? \t"))
                    
                    for count, value in enumerate(record):
                        if value[0] == int(id_input):
                            print("| id | - | service | - | username | - | password |\n")
                            print(
                            f"| {value[0]} | - | {value[1]} | - | {value[2]} | - | {value[3]} |\n")
                            break
                    
                    print("Type 'no' & press ENTER to not modify values\n")
                    
                    service_input = input("Update service name : \t")
                    input_dict.update({"service": service_input})
                    
                    identifiant_input = input("Update identifiant : \t")
                    input_dict.update({"identifiant": identifiant_input})

                    mdp_input = input("Update password : \t")
                    input_dict.update({"mdp": mdp_input})

                    sql_query = "update passwords set "
                    counter = 0 

                    for key, value in input_dict.items():
                        if str(value).lower() != 'no':
                            if counter == 0:
                                sql_query+=f"{key} = '{value}' "
                            else:
                                sql_query+=f", {key} = '{value}' "
                            counter += 1
                    
                    sql_query+=f"where id = {id_input}"
                 
                    if sql_query != f"update passwords set where id = {id_input}":
                        cursor.execute(
                                sql_query)
                        connection.commit()
                        print("Record updated !")
                        cursor.close()

                elif user_input == '4':
                    cursor.execute("select * from passwords;")
                    record = cursor.fetchall()
                    print("| id | - | service |")
                    for count, value in enumerate(record):
                        print(
                            f"| {value[0]} | - | {value[1]} |\n")
                    id_input = int(
                        input("Which record do you want to delete ? \t"))
                    cursor.execute(
                        f"delete from passwords where id = {id_input} ")
                    connection.commit()
                    print("Record deleted !")
                    cursor.close()

                else:
                    break

except Error as e:
    print("Error while connecting to MySQL", e)
    
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
