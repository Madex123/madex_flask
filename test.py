import sqlite3

connection = sqlite3.connect('flask_training.db')

cursor = connection.cursor()

create_table = 'create table users (id int, username text, password text)'

cursor.execute(create_table)

user = [(2, 'rolf', 'asdf'), (3, 'anne', 'xyz')]

insert_query = 'insert into users values (?, ?, ?)'
cursor.executemany(insert_query, user) # cursor knows to replace questionmarks with tuple

select_query = "select * from users"
for row in cursor.execute(select_query):
    print(row)

connection.commit()

connection.close()