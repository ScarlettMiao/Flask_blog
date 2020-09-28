import sqlite3

connection = sqlite3.connect('database.db')

#use the open() function to open the schema.sql file
with open('schema.sql') as f:
    connection.executescript(f.read())

#execute its contents using the executescript() method that executes 
#multiple SQL statements at once, which will create the posts table
cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('First Post', 'Content for the first post')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second Post', 'Content for the second post')
            )

connection.commit()
connection.close()