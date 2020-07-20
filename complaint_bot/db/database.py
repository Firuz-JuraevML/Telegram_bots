import sqlite3 

conn = sqlite3.connect("bbc_db.db")

conn.execute('''CREATE TABLE user_step
             (user_id TEXT PRIMARY KEY NOT NULL, 
             user_name TEXT, 
             fullname TEXT, 
             language TEXT, 
             phone TEXT, 
             region TEXT,
             complain TEXT, 
             step TEXT);''') 

conn.close() 
