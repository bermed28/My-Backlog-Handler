from getpass import getpass
from psycopg2 import connect, Error

try:
    with connect(
            host="ec2-3-221-243-122.compute-1.amazonaws.com",
            user='pstrvwkgawgebj',
            password='2a3e09653b512133580a42e74a224a7c66b2cacc0e475bc32b45bebefac1d402',
            port='5432',
            database='d3ufdgbv33stba'
    ) as connection:
        print(connection)

        with connection.cursor() as cursor:
             cursor.execute("CREATE SCHEMA TestingDB")

        

except Error as e:
    print(e)
