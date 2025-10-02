import mysql.connector
from mysql.connector import Error
from dataclasses import dataclass, field
import random
from cryptography.fernet import Fernet
from dotenv import dotenv_values
import glob
import csv

@dataclass(frozen=False)
class Query_manager:
    connection: mysql
    key: bytes = field(init=False)
    config: dict = field(init=False, default_factory=dict)
    
    def __post_init__(self) -> None:
        # self.connection = mysql.connector.connect(host = self.host, database = self.database, user = self.user,password = self.password)
        if self.connection.is_connected():
            db_Info = self.connection.get_server_info()
            self.config = dotenv_values(".env")
            print("Connected to MySQL Server version ", db_Info)
            if not glob.glob("logs/key.txt"):
                print("Genereting key...")
                self.key = Fernet.generate_key()
                with open("logs/key.txt", "wb") as f:
                    f.write(self.key)
            else:
                with open("logs/key.txt", "rb") as f:
                    self.key = f.read()
        else:
            print("Error while connecting to MySQL", Error)
    
    def search_password(self, search_value) -> None:
        cursor = self.connection.cursor()
        cursor.execute(f"select * from {self.config['TABLE']} where service like %s;", (f"%{search_value}%",))
        record = cursor.fetchall()
        print("| id | - | service |")
        for count, value in enumerate(record):
            print(
                f"| {value[0]} | - | {value[1]} |\n")
        cursor.close()
        
    def generate_password(self, length: int) -> str:
        characters: str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@%^&*_+|:"<>,.;?'
        password: str = ""
        random_string: str = ""
        for i in range(length):
            password += random.choice(characters)
        print(f"Your password is : {password}")
        return password
    
    def display_all_passwords(self) -> None:
        cursor = self.connection.cursor()
        cursor.execute(f"select * from {self.config['TABLE']};")
        record = cursor.fetchall()
        print("| id | - | service |")
        for count, value in enumerate(record):
            print(
                f"| {value[0]} | - | {value[1]} |\n")
        cursor.close()
    
    def display_password(self, id) -> None:
        fernet = Fernet(self.key)
        cursor = self.connection.cursor()
        cursor.execute(f"select * from {self.config['TABLE']} where id = %s;", (id,))
        record = cursor.fetchall()
        
        if len(record) == 0:
            print("No password found")
            return None
        else:
            print("| id | - | service | - | username | - | password |\n")
            for count, value in enumerate(record):
                print(
                    f"| {value[0]} | - | {value[1]} | - | {value[2]} | - | {fernet.decrypt(bytes(value[3], 'utf-8')).decode()} |\n")
                return None
        cursor.close()
    
    def add_password(self) -> None:
        fernet = Fernet(self.key)
        cursor = self.connection.cursor()
        service = input("Input service name : \t")
        identifiant = input("Input username : \t")
        mdp = input("Type your password (leave blank to generate a random password): \t")
        mdp = mdp or self.generate_password(20)
        cursor.execute(
            f"insert into {self.config['TABLE']} (service, identifiant, mdp) values (%s, %s, %s);",
            (service, identifiant, fernet.encrypt(mdp.encode()))
        )
        self.connection.commit()
        print("Password added")
        cursor.close()
    
    def edit_password(self, id) -> None:
        fernet = Fernet(self.key)
        cursor = self.connection.cursor()
        cursor.execute(f"select * from {self.config['TABLE']} where id = %s;", (id,))
        record = cursor.fetchall()
        input_dict = {}
        
        if len(record) == 0:
            print("No password found")
            return None
        
        # Display password
        self.display_password(id)     
        
        print("Leave blank and press ENTER to not modify values\n")
        service_input = input("Update service name : \t")
        input_dict.update({"service": service_input})
        
        identifiant_input = input("Update identifiant : \t")
        input_dict.update({"identifiant": identifiant_input})

        mdp_input = input("Update password : \t")
        if mdp_input:
            mdp_input = fernet.encrypt(mdp_input.encode())
        else:
            mdp_input = record[0][3]
        
        input_dict.update({"mdp": mdp_input})

        sql_query = f"update {self.config['TABLE']} set "
        counter = 0 

        for key, value in input_dict.items():
            if str(value).lower() != '':
                if counter == 0:
                    if key == "mdp":
                        sql_query+=f"{key} = %s "
                    else:
                        sql_query+=f"{key} = '{value}' "
                elif key == "mdp":
                    sql_query+=f", {key} = %s "
                else:
                    sql_query+=f", {key} = '{value}' "
                counter += 1
        
        sql_query+=f"where id = {id}"

        if sql_query != f"update {self.config['TABLE']} set where id = {id}":
            cursor.execute(
                    sql_query, 
                    (mdp_input,)
                )
            self.connection.commit()
            print("Record updated !")
        else:
            print("\nNo changes made")   
        cursor.close()
        
    def delete_password(self, id) -> None:
        cursor = self.connection.cursor()
        cursor.execute(f"select * from {self.config['TABLE']} where id = %s;", (id,))
        record = cursor.fetchall()
        
        if len(record) == 0:
            print("No password found")
            return None
        
        cursor.execute(
            f"delete from {self.config['TABLE']} where id = %s ", 
            (id,)
        )
        self.connection.commit()
        print("Record deleted !")
        cursor.close()
    
    def export_passwords(self, option: bool) -> None:
        fernet = Fernet(self.key)
        cursor = self.connection.cursor()
        cursor.execute(f"select * from {self.config['TABLE']};")
        record = cursor.fetchall()
        if len(record) == 0:
            print("No password found")
            return None
        else:
            with open("logs/passwords.csv", "w") as file:
                writer = csv.writer(file)
                writer.writerow(["id", "service", "username", "password"])
                for count, value in enumerate(record):
                    writer.writerow([value[0], value[1], value[2], value[3] if not option else fernet.decrypt(bytes(value[3], 'utf-8')).decode()])
                print("Passwords exported to passwords.csv !")

        cursor.close()
    
    def close_connection(self) -> None:
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")
        else:
            print("Error while closing connection")
        
    
    