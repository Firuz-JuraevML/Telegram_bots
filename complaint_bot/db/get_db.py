import sqlite3 

conn = sqlite3.connect("bbc_db.db")

cursor = conn.execute("SELECT * FROM user_step;") 

for row in cursor:
    print (row) 

print ("Operation done successfully")
conn.close()