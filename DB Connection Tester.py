from getpass import getpass
from mysql.connector import connect, Error

try:
    with connect(
            host="mydb.cgvx1gn2r43i.us-east-2.rds.amazonaws.com",
            user= 'admin',
            password= 'newrootpassword',
            port = '5000',
            database = 'dbtest'
    ) as connection:
        print(connection)

except Error as e:
    print(e)