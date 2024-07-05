import mysql.connector

conexion = mysql.connector.connect(user='admin',
                                   password='',
                                   host='localhost1',
                                   database='test',
                                   port='3310')

print(conexion)