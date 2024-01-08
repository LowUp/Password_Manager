import mysql.connector
from mysql.connector import Error
from dataclasses import dataclass
import random

@dataclass(frozen=True)
class Query_manager:
    connection: mysql
    
    def __post_init_(self) -> None:
        # self.connection = mysql.connector.connect(host = self.host, database = self.database, user = self.user,password = self.password)
        if self.connection.is_connected():
            db_Info = self.connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
        else:
            print("Error while connecting to MySQL", Error)
    
    def search_password(self, search_value) -> None:
        cursor = self.connection.cursor()
        cursor.execute(f"select * from passwords where service like %s;", (f"%{search_value}%",))
        record = cursor.fetchall()
        print("| id | - | service |")
        for count, value in enumerate(record):
            print(
                f"| {value[0]} | - | {value[1]} |\n")
        cursor.close()
        
    def generate_password(self, length: int) -> str:
        characters: str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:<>,./?'
        password: str = ""
        random_string: str = ""
        for i in range(length):
            password += random.choice(characters)
        print(f"Your password is : {password}")
        return password
    
    def display_all_passwords(self) -> None:
        cursor = self.connection.cursor()
        cursor.execute("select * from passwords;")
        record = cursor.fetchall()
        print("| id | - | service |")
        for count, value in enumerate(record):
            print(
                f"| {value[0]} | - | {value[1]} |\n")
        cursor.close()
    
    def display_password(self, id) -> None:
        cursor = self.connection.cursor()
        cursor.execute(f"select * from passwords where id = %s;", (id,))
        record = cursor.fetchall()
        
        if len(record) == 0:
            print("No password found")
            return None
        else:
            print("| id | - | service | - | username | - | password |\n")
            for count, value in enumerate(record):
                print(
                    f"| {value[0]} | - | {value[1]} | - | {value[2]} | - | {value[3]} |\n")
                return None
        cursor.close()
    
    def add_password(self) -> None:
        cursor = self.connection.cursor()
        service = input("Input service name : \t")
        identifiant = input("Input username : \t")
        mdp = input("Type your password (leave blank to generate a random password): \t")
        mdp = mdp or self.generate_password(20)
        cursor.execute(
            f"insert into passwords (service, identifiant, mdp) values (%s, %s, %s);", 
            (service, identifiant, mdp)
        )
        self.connection.commit()
        print("Password added")
        cursor.close()
    
    def edit_password(self, id) -> None:
        cursor = self.connection.cursor()
        cursor.execute(f"select * from passwords where id = %s;", (id,))
        record = cursor.fetchall()
        input_dict = {}
        
        if len(record) == 0:
            print("No password found")
            return None
        
        for count, value in enumerate(record):
            print("| id | - | service | - | username | - | password |\n")
            print(
            f"| {value[0]} | - | {value[1]} | - | {value[2]} | - | {value[3]} |\n")
        
        print("Leave blank and press ENTER to not modify values\n")
        service_input = input("Update service name : \t")
        input_dict.update({"service": service_input})
        
        identifiant_input = input("Update identifiant : \t")
        input_dict.update({"identifiant": identifiant_input})

        mdp_input = input("Update password : \t")
        input_dict.update({"mdp": mdp_input})

        sql_query = "update passwords set "
        counter = 0 

        for key, value in input_dict.items():
            if str(value).lower() != '':
                if counter == 0:
                    sql_query+=f"{key} = '{value}' "
                else:
                    sql_query+=f", {key} = '{value}' "
                counter += 1
        
        sql_query+=f"where id = {id}"
        
        if sql_query != f"update passwords set where id = {id}":
            cursor.execute(
                    sql_query)
            self.connection.commit()
            print("Record updated !")
        else:
            print("\nNo changes made")   
        cursor.close()
        
    def delete_password(self, id) -> None:
        cursor = self.connection.cursor()
        cursor.execute(f"select * from passwords where id = %s;", (id,))
        record = cursor.fetchall()
        
        if len(record) == 0:
            print("No password found")
            return None
        
        cursor.execute(
            f"delete from passwords where id = %s ", 
            (id,)
        )
        self.connection.commit()
        print("Record deleted !")
        cursor.close()
    
    def close_connection(self) -> None:
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")
        else:
            print("Error while closing connection")
        
    
    