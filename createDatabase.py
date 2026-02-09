#to be able to use python built in support for SQlite
import sqlite3
# to be able to read csv files
import csv 

#create a sqlite database
connection = sqlite3.connect('database.db')



# Sql to create table if it doesnt exists
create_pokedex_table = '''CREATE TABLE IF NOT EXISTS pokedex(
               
                entry INTEGER,
                name TEXT NOT NULL,
                type1 TEXT NOT NULL,
                type2 TEXT NOT NULL DEFAULT '',
                generation INTEGER,
                legendary  TEXT NOT NULL,
                PRIMARY KEY (name)
                );
                '''

# Creating the table into our database
connection.execute(create_pokedex_table)





#open csv file 
file = open('poke.csv')
# read csv file contents
contents = csv.reader(file)
#SQl to insert or replace contents into pokdex table
insert_records = "INSERT OR REPLACE INTO pokedex (entry,name, type1, type2, generation, legendary ) VALUES(?,?, ?,?,?,?)"

# execute content from csv file into pokdex table 
connection.executemany(insert_records, contents)
connection.commit()
# Sql to create table if it doesnt exists
create_favorites_table = '''CREATE TABLE IF NOT EXISTS favorites(
                
                entry INTEGER,
                name TEXT NOT NULL,
                type1 TEXT NOT NULL,
                type2 TEXT NOT NULL DEFAULT '',
                generation INTEGER,
                legendary  TEXT NOT NULL,
                PRIMARY KEY (name)
                );
                '''
connection.execute(create_favorites_table)
insert_poke_records = "INSERT OR REPLACE INTO favorites (entry,name, type1, type2, generation, legendary ) VALUES(?,?, ?,?,?,?)"
connection.execute(insert_poke_records, (1,"Bulbasaur","Grass","Poison",1,"FALSE"))
connection.execute(create_favorites_table)



# This method commits the current transaction. If you don't call this method, anything you did since the last call to commit() is not visible from other database connections.
connection.commit()
create_createPokemon_table = '''CREATE TABLE IF NOT EXISTS createPokemon(
                name TEXT NOT NULL,
                type1 TEXT NOT NULL,
                type2 TEXT NOT NULL DEFAULT '',
                legendary  TEXT NOT NULL,
                PRIMARY KEY (name)
                );
                '''
connection.execute(create_createPokemon_table)
insert_create_records = "INSERT OR REPLACE INTO createPokemon(name, type1, type2,legendary ) VALUES(?,?, ?,?)"
connection.execute(insert_create_records, ("Bilbo","Fairy","Dragon","FALSE"))
connection.execute(create_createPokemon_table)
connection.commit()

# closing the database connection
connection.close()


