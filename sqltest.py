import mysql.connector
import time
c = mysql.connector.connect(user = "root", password = "dwttddhmis619", host = "localhost", database = "GridL")
add_employee = ("INSERT INTO moves "
               "(UserID, Time, PositionX, PositionY, Piece, Confirmed) "
               "VALUES (%s, %s, %s, %s, %s, %s)")
cursor = c.cursor()
for i in range (1,5):
    cursor.execute(add_employee, (-1 - i, time.time(), -1, -1, -1, False))


cursor.execute("SELECT * FROM moves ORDER BY UserID")

print(cursor.fetchall())
#for (Time) in cursor:
#    print(Time)

cursor.close()
c.close()