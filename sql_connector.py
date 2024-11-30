import mysql.connector

conn = mysql.connector.connect(host = 'localhost', user = 'root', password = 'your_password')

if conn.is_connected():
    print('connected')

mycursor = conn.cursor()
mycursor.execute("CREATE DATABASE whatsapp_db")
print(mycursor)
