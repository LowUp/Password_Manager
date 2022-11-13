import mysql.connector
from mysql.connector import Error
from dotenv import dotenv_values

config = dotenv_values(".env")


try:
    if input("Master password : \t") != config['MASTER_KEY']:
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
                    "\n*****************************************\n\t1 - List all passwords\n\t2 - Add a password\n\t3 - Update a record\n\t4 - Delete a record\n\tAny other key - exit\n*****************************************\n")
                cursor = connection.cursor()
                if user_input == '1':
                    cursor.execute("select * from passwords;")
                    record = cursor.fetchall()
                    print(f"| id | - | service | - | password |")
                    for count, value in enumerate(record):
                        print(
                            f"| {value[0]} | - | {value[1]} | - | {value[2]} | \n")

                elif user_input == '2':
                    service = input("Input service name : \t")
                    mdp = input("Type your password : \t")
                    cursor.execute(
                        f"insert into passwords (service, mdp) values ('{service}', '{mdp}');")
                    connection.commit()
                    print(cursor.rowcount,
                        "Data inserted !")
                    cursor.close()

                elif user_input == '3':
                    cursor.execute("select * from passwords;")
                    record = cursor.fetchall()
                    print(f"| id | - | service | - | password |")
                    for count, value in enumerate(record):
                        print(
                            f"| {value[0]} | - | {value[1]} | - | {value[2]} | \n")
                    id_input = int(input("Which one do you want to update ? \t"))
                    service_input = input("Update service name : \t")
                    mdp_input = input("Update password : \t")
                    cursor.execute(
                        f"update passwords set service = '{service_input}', mdp = '{mdp_input}' where id = {id_input} ")
                    connection.commit()
                    print("Record updated !")
                    cursor.close()

                elif user_input == '4':
                    cursor.execute("select * from passwords;")
                    record = cursor.fetchall()
                    print(f"| id | - | service | - | password |")
                    for count, value in enumerate(record):
                        print(
                            f"| {value[0]} | - | {value[1]} | - | {value[2]} | \n")
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
