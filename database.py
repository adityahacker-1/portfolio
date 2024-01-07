import mysql.connector

db = mysql.connector.connect(host="localhost",user="sahil",password="P@ssw0rd123",database="login")
cursor = db.cursor()

username = input("Enter the name: ")
email = input("Enter your email: ")
password = input("Enter the password: ")

cursor.execute("""

    INSERT INTO `users` (`username`,`email`,`password`) VALUES ('{}','{}','{}');
""".format(username,email,password)
)

db.commit()

cursor.execute("""
    SELECT * FROM users WHERE username LIKE '{}';               
""".format(username)
)

data = cursor.fetchall()
print(data)
