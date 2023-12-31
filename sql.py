import mysql.connector

"""This file consists of mysql database connection details. It extracts the unique ID numbers 
saved in the database and returns all the details in a list format"""

def sql_connection():
        conn = mysql.connector.connect(
            host = "localhost",
            password = "jala007aA",
            user = "root",
            database = "Formrecognizer"
        )
        cursor = conn.cursor()
        cursor.execute("select * from aadhar")
        res = cursor.fetchall()
        lis = []
        for row in res:
            for i in row:
                lis.append(i)
        return(lis)

