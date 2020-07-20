import sqlite3 

conn = sqlite3.connect("bbc_db.db")

cursor = conn.execute("DELETE FROM user_step;") 

conn.commit()
print ("Operation done successfully")
conn.close()