from getpass import getpass
from mysql.connector import connect, Error

try:
    with connect(
            host="mydb.cgvx1gn2r43i.us-east-2.rds.amazonaws.com",
            user='admin',
            password='newrootpassword',
            port='5000',
            # database = 'testingDB'
    ) as connection:
        print(connection)
        with connection.cursor() as cursor:
            cursor.execute("SHOW DATABASES")

except Error as e:
    print(e)
