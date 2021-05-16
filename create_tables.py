import sqlite3

connection = sqlite3.connect('flask_training.db')

cursor = connection.cursor()

create_table = "create table if not exists users (id integer primary key, username text, password text)"  # if you need auto increment specify integer primary key as a data type
cursor.execute(create_table)

create_table = "create table if not exists items (name text, price real)"
cursor.execute(create_table)

connection.close()
