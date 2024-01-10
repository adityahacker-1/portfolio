import mysql.connector

class Database:
    def __init__(self):
        
        self.db = mysql.connector.connect(host="localhost",user="sahil",password="P@ssw0rd123",database="login")
        self.cursor = self.db.cursor()
        
        

    def register(self,email,password,username,firstname,lastname):
        # username = input("Enter the name: ")
        # email = input("Enter your email: ")
        # password = input("Enter the password: ")
        
        self.cursor.execute("""

            INSERT INTO `users` (`username`,`email`,`password`,`firstname`,`lastname`) VALUES ('{}','{}','{}','{}','{}');
        """.format(username,email,password,firstname,lastname)
        )

        self.db.commit()
    

    # def search_password(self,email):
    #     self.cursor.execute("""
    #         SELECT * FROM users WHERE email LIKE '{}';               
    #     """.format(email)
    #     )

    #     data = self.cursor.fetchall()
    #     return data[-3]
