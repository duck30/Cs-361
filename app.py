# TODO: still have to do create, update functionality
#CRUD - CREATER READ UPDATER DELETE
#DELETE - DONE
#READ -DONE
# UPDATE INCOMPLETE
#CREATE INCOMPLETE

#finsiuh search page first the do CREATE and UPDATE
#CREATE AND UPDATE ARE TIED TOGETHER 
# FINSIH CREATE FIRST THEN AFFTER WE DO UPDATE
#CHECK TO DO TXT FILE 




# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import os
# to be able to use flask, json, and to use tempklates from frontend/templates folder
from flask import Flask, json, redirect, render_template, request
#to be able to use python built in support for SQlite
import sqlite3

#from flask_mysqldb import MySQL


# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__, template_folder="frontend/templates")
#mysql = MySQL(app)

# The route() decorator in Flask is used to bind URL to a function
# url "/" is bound to fucntion home() 
@app.route("/")
def home():

    # function render_template() renders jinja2 file "index.j2" from frontend/temnpkates folder. 
    return render_template("home.j2")

#HTTP methods 
# 'GET' to request data from the server
#'POST 'method is used to send data to the server for processing
#methods = ['POST','GET']
@app.route("/Pokedex", methods = ['GET'])
def pokdex():
    if request.method == "GET":
        # connect to databse
        connection = sqlite3.connect("database.db")
        #this is for displaying the rows of data 
        connection.row_factory = sqlite3.Row
        #creates a cursor. This method accepts a single optional parameter cursorClass
        cur = connection.cursor()
        #This routine executes an SQL statement. The SQL statement may be parameterized  (i. e. placeholders instead of SQL literals)
        cur.execute("SELECT * FROM pokedex")
        #This routine fetches all (remaining) rows of a query result, returning a list. An empty list is returned when no rows are available.
        data = cur.fetchall();
        #sends data from to jinja2 file "pokedex.j2" for rendering/dsiplay
        return render_template("pokedex.j2",data = data)
    
# add pokeon to favorites from pkdex page 
@app.route("/add_pokemon/<string:name>")
def add_pokemon_to_favorites(name):

    #add pokemon
    query = "INSERT OR REPLACE INTO favorites (entry,name, type1, type2, generation, legendary ) SELECT entry,name, type1, type2, generation, legendary FROM pokedex WHERE name = ?;"
    connection = sqlite3.connect("database.db")
    cur = connection.cursor()
    cur.execute(query,(name,))
    connection.commit()



    return redirect("/Pokedex")   


#this page is for displaying favorite pokemon
@app.route("/Favorites",methods = ['POST','GET'])
def favorites():

  
    if request.method == "GET":
        # connect to databse
        connection = sqlite3.connect("database.db")
        #this is for displaying the rows of data 
        connection.row_factory = sqlite3.Row
        #creates a cursor. This method accepts a single optional parameter cursorClass
        cur = connection.cursor()
        #This routine executes an SQL statement. The SQL statement may be parameterized  (i. e. placeholders instead of SQL literals)
        cur.execute("SELECT * FROM favorites")
        #This routine fetches all (remaining) rows of a query result, returning a list. An empty list is returned when no rows are available.
        favorite = cur.fetchall();
    
        
    return render_template("favorites.j2", favorite= favorite)
# delete pokmeon from favorites page
@app.route("/delete_pokemon/<string:name>")
def delete_characters(name):

    #Delete pokemon
    query = "DELETE FROM favorites WHERE name= ?;"
    connection = sqlite3.connect("database.db")
    cur = connection.cursor()
    cur.execute(query,(name,))
    connection.commit()
    

    return redirect("/Favorites")

#this page is for searchijng up pokemon to add to favorites 
@app.route("/Search",methods = ['POST','GET'])
def search():
    if request.method == "POST":

        #this is when they submmitted seacrh form
        # this is displays pokjemon using criteria the user chose 
        if request.form.get("Search_Pokemon"):

            #INPUTS entry 	name 	type1 	type2 	generation 	legendary
            # only entry and geration are integers evrtythign else is text
            # if uses number use "" if it is null else if it is string use "0"
            #entry= request.form["entry"]
            #name= request.form["type1"]
            type1= request.form["type1"]
            type2= request.form["type2"]
            generation= request.form["generation"]
            legendary= request.form["legendary"]
            
            connection = sqlite3.connect("database.db")
            connection.row_factory = sqlite3.Row

            # ***************** for when TYPE1 or TYPE2 is null *******************************
            
                
            # this is when type1 is null and type2 is null or 0
            if (type2 == "null" or type1 =="null") and generation =="null" and legendary == "null":
                
                # this is if type 1 is null and type2 is 0 
                # this dsipalys all pokemon with only 1 type
                if type1 == "null" and type2 == "0":
                    type1_query = "SELECT * FROM pokedex WHERE type2 = ''"
                    cur = connection.cursor()
                    cur.execute(type1_query)

                #this is if type1 is null  make type 1 be of type2
                # this is dislays all pokemon of that has that type 
                elif type1 == "null":
                    type1 = type2
                    type1_query = "SELECT * FROM pokedex WHERE type1 = ? OR type2 = ?;"
                    cur = connection.cursor()
                    cur.execute(type1_query,(type1,type1))

                else: 

                    type1_query = "SELECT * FROM pokedex WHERE type1 = ? OR type2 = ?;"
                    cur = connection.cursor()
                    cur.execute(type1_query,(type1,type1))
                
                
                
                show = cur.fetchall();
                connection.commit()
                query = "SELECT DISTINCT type1 AS 'TYPE' FROM pokedex"
            
                cur = connection.cursor()
                cur.execute(query)
                data = cur.fetchall()


             
            elif (type2 == "null" or type1 =="null") and generation =="null" :
                if type1 == "null" and type2 == "0":
                    type1_query = "SELECT * FROM pokedex WHERE type2 = '' AND legendary = ?"
                    cur = connection.cursor()
                    cur.execute(type1_query,(legendary,))

                
                elif type2 =="null" and type1 != "null":
                    
                    type1_query = "SELECT * FROM pokedex WHERE (type1 = ? OR type2 = ?) AND legendary = ?"
                    cur = connection.cursor()
                    cur.execute(type1_query,(type1,type1,legendary,))
        
                else: 
                    
                    type1_query = "SELECT * FROM pokedex WHERE  legendary = ?"
                    cur = connection.cursor()
                    cur.execute(type1_query,(legendary,))
                
                
                show = cur.fetchall();
                connection.commit()
                query = "SELECT DISTINCT type1 AS 'TYPE' FROM pokedex"
            
                cur = connection.cursor()
                cur.execute(query)
                data = cur.fetchall()

            
            elif (type2 == "null" or type1 =="null") and legendary == "null":
                
                # this is if type 1 is null and type2 is 0 
                # this dsipalys all pokemon with only 1 type

                
                if type1 == "null" and type2 == "0":
                    type1_query = "SELECT * FROM pokedex WHERE type2 = '' AND generation = ?"
                    cur = connection.cursor()
                    cur.execute(type1_query,(generation,))

                
                elif type2 =="null" and type1 != "null":
                    
                    type1_query = "SELECT * FROM pokedex WHERE (type1 = ? OR type2 = ?) AND generation = ?"
                    cur = connection.cursor()
                    cur.execute(type1_query,(type1,type1,generation,))
                elif type1 =="null" and type2 != "null":
                    
                    type1_query = "SELECT * FROM pokedex WHERE (type1 = ? OR type2 = ?) AND generation = ?"
                    cur = connection.cursor()
                    cur.execute(type1_query,(type2,type2,generation,))
        
                else: 
                    
                    type1_query = "SELECT * FROM pokedex WHERE  generation = ?"
                    cur = connection.cursor()
                    cur.execute(type1_query,(generation,))
                
                
                show = cur.fetchall();
                connection.commit()
                query = "SELECT DISTINCT type1 AS 'TYPE' FROM pokedex"
            
                cur = connection.cursor()
                cur.execute(query)
                data = cur.fetchall()


              
            elif (type2 == "null" or type1 =="null") :

                if type1 == "null" and type2 == "0":
                    type1_query = "SELECT * FROM pokedex WHERE type2 = '' AND generation = ? AND legendary = ?"
                    cur = connection.cursor()
                    cur.execute(type1_query,(generation,legendary))

                
                elif type2 =="null" and type1 != "null":
                    
                    type1_query = "SELECT * FROM pokedex WHERE (type1 = ? OR type2 = ?) AND generation = ?  AND legendary = ?"
                    cur = connection.cursor()
                    cur.execute(type1_query,(type1,type1,generation,legendary))
                elif type1 =="null" and type2 != "null":
                    
                    type1_query = "SELECT * FROM pokedex WHERE (type1 = ? OR type2 = ?) AND generation = ?  AND legendary = ?"
                    cur = connection.cursor()
                    cur.execute(type1_query,(type2,type2,generation,legendary))
        
                else: 
                    
                    type1_query = "SELECT * FROM pokedex WHERE  generation = ?  AND legendary = ?"
                    cur = connection.cursor()
                    cur.execute(type1_query,(generation,legendary))
                
                
                show = cur.fetchall();
                connection.commit()
                query = "SELECT DISTINCT type1 AS 'TYPE' FROM pokedex"
            
                cur = connection.cursor()
                cur.execute(query)
                data = cur.fetchall()
            # ***************** for when TYPE2  == "0" *******************************
            
            elif type2 == "0"  and generation =="null" and legendary == "null":

                type1_query = "SELECT * FROM pokedex WHERE type1 = ? AND type2 = '' ;"
                cur = connection.cursor()
                cur.execute(type1_query,(type1,))
                show = cur.fetchall();
                connection.commit()
                query = "SELECT DISTINCT type1 AS 'TYPE' FROM pokedex"
            
                cur = connection.cursor()
                cur.execute(query)
                data = cur.fetchall()
            elif type2 == "0"  and generation =="null" :
                type1_query = "SELECT * FROM pokedex WHERE type1 = ? AND type2 = '' AND legendary = ? ;"
                cur = connection.cursor()
                cur.execute(type1_query,(type1,legendary))
                show = cur.fetchall();
                connection.commit()
                query = "SELECT DISTINCT type1 AS 'TYPE' FROM pokedex"
            
                cur = connection.cursor()
                cur.execute(query)
                data = cur.fetchall()

            elif type2 == "0"  and legendary == "null":
                type1_query = "SELECT * FROM pokedex WHERE (type1 = ? AND type2 ='')  AND generation = ?;"
                cur = connection.cursor()
                cur.execute(type1_query,(type1,generation))
                show = cur.fetchall();
                connection.commit()
                query = "SELECT DISTINCT type1 AS 'TYPE' FROM pokedex"
            
                cur = connection.cursor()
                cur.execute(query)
                data = cur.fetchall()

            elif type2 == "0":
                type1_query = "SELECT * FROM pokedex WHERE type1 = ? AND type2 = ''  AND generation = ? AND legendary = ?;"
                cur = connection.cursor()
                cur.execute(type1_query,(type1,generation,legendary))
                show = cur.fetchall();
                connection.commit()
                query = "SELECT DISTINCT type1 AS 'TYPE' FROM pokedex"
            
                cur = connection.cursor()
                cur.execute(query)
                data = cur.fetchall() 

           #*************************     FOR WHEN TYPE1 and TYPE2 is anwered either null or 0 **********************************************************************************************
            elif generation =="null" and legendary == "null":
                
                type1_query = "SELECT * FROM pokedex WHERE (type1 = ? OR  type1 = ?) AND (type2 = ? OR type2 = ?) ;"
                cur = connection.cursor()
                cur.execute(type1_query,(type1,type2,type1,type2))
                show = cur.fetchall();
                connection.commit()
                query = "SELECT DISTINCT type1 AS 'TYPE' FROM pokedex"
            
                cur = connection.cursor()
                cur.execute(query)
                data = cur.fetchall()
            
            elif generation == "null":
                type1_query = "SELECT * FROM pokedex WHERE (type1 = ? OR  type1 = ?) AND (type2 = ? OR type2 = ?) AND legendary = ? ;"
                cur = connection.cursor()
                cur.execute(type1_query,(type1,type2,type1,type2,legendary))
                show = cur.fetchall();
                connection.commit()
                query = "SELECT DISTINCT type1 AS 'TYPE' FROM pokedex"
            
                cur = connection.cursor()
                cur.execute(query)
                data = cur.fetchall()
                

            elif legendary == "null":
                type1_query = "SELECT * FROM pokedex WHERE (type1 = ? OR  type1 = ?) AND (type2 = ? OR type2 = ?) AND generation = ? ;"
                cur = connection.cursor()
                cur.execute(type1_query,(type1,type2,type1,type2,generation))
                show = cur.fetchall();
                connection.commit()
                query = "SELECT DISTINCT type1 AS 'TYPE' FROM pokedex"
            
                cur = connection.cursor()
                cur.execute(query)
                data = cur.fetchall()

            else:
                type1_query = "SELECT * FROM pokedex WHERE (type1 = ? OR  type1 = ?) AND (type2 = ? OR type2 = ?) AND generation = ? AND legendary = ?;"
                cur = connection.cursor()
                cur.execute(type1_query,(type1,type2,type1,type2,generation,legendary))
                show = cur.fetchall();
                connection.commit()
                query = "SELECT DISTINCT type1 AS 'TYPE' FROM pokedex"
            
                cur = connection.cursor()
                cur.execute(query)
                data = cur.fetchall()


            

            
                
            
        
            return render_template("search.j2",data = data,show = show)

    
       
    
    if request.method == "GET":
        
        query = "SELECT DISTINCT type1 AS 'TYPE' FROM pokedex"
        connection = sqlite3.connect("database.db")
        connection.row_factory = sqlite3.Row
        cur = connection.cursor()

        cur.execute(query)
        data = cur.fetchall()
        
        
        return render_template("search.j2",data= data)
    
# add pokeon to favorites from pkdex page 
@app.route("/add_search_pokemon/<string:name>")
def add_search_pokemon_to_favorites(name):

    #add pokemon
    query = "INSERT OR REPLACE INTO favorites (entry,name, type1, type2, generation, legendary ) SELECT entry,name, type1, type2, generation, legendary FROM pokedex WHERE name = ?;"
    connection = sqlite3.connect("database.db")
    cur = connection.cursor()
    cur.execute(query,(name,))
    connection.commit()

    return redirect("/Search")  



@app.route("/Create",methods = ['POST','GET'])
def createPokemon():
    if request.method == "POST":

        #this is when they submmitted seacrh form
        # this is displays pokjemon using criteria the user chose 
        if request.form.get("Create_Pokemon"):

            #INPUTS entry 	name 	type1 	type2 	generation 	legendary
            # only entry and geration are integers evrtythign else is text
            # if uses number use "" if it is null else if it is string use "0"
            #entry= request.form["entry"]
            name= request.form["name"]
            type1= request.form["type1"]
            type2= request.form["type2"]
            legendary= request.form["legendary"]
    
            query = "INSERT OR REPLACE INTO createPokemon (name, type1, type2,legendary ) VALUES(?,?, ?,?)"
            connection = sqlite3.connect("database.db")
            cur = connection.cursor()
            cur.execute(query,(name,type1,type2,legendary))
            connection.commit()
            
            connection.row_factory = sqlite3.Row
            
            query = "SELECT DISTINCT type1 AS 'TYPE' FROM pokedex"

            cur = connection.cursor()

            cur.execute(query)
            data = cur.fetchall()
            cur = connection.cursor()
            cur.execute("SELECT * FROM createPokemon")
            connection = sqlite3.connect("database.db")
            show = cur.fetchall();
            cur.execute("SELECT name FROM createPokemon")
            connection = sqlite3.connect("database.db")
            names = cur.fetchall();
        
        elif request.form.get("Edit_Pokemon"):

            name= request.form["name"]
            type1= request.form["type1"]
            type2= request.form["type2"]
            legendary= request.form["legendary"]
            
            query = "UPDATE  createPokemon SET type1 = ?, type2 = ?, legendary = ? WHERE name = ? "
           
            connection = sqlite3.connect("database.db")
            cur = connection.cursor()

            cur.execute(query,(type1,type2, legendary,name))
            connection.commit()
            query = "SELECT DISTINCT type1 AS 'TYPE' FROM pokedex"
            connection = sqlite3.connect("database.db")
            connection.row_factory = sqlite3.Row
            cur = connection.cursor()

            cur.execute(query)
            data = cur.fetchall()
            connection.row_factory = sqlite3.Row
            cur = connection.cursor()
            cur.execute("SELECT * FROM createPokemon")
            connection = sqlite3.connect("database.db")
            show = cur.fetchall();
            cur.execute("SELECT name FROM createPokemon")
            connection = sqlite3.connect("database.db")
            names = cur.fetchall();
        return render_template("create.j2", data = data, show = show,created_names= names)


    if request.method == "GET":
        
        query = "SELECT DISTINCT type1 AS 'TYPE' FROM pokedex"
        connection = sqlite3.connect("database.db")
        connection.row_factory = sqlite3.Row
        cur = connection.cursor()

        cur.execute(query)
        data = cur.fetchall()
        connection.row_factory = sqlite3.Row
        cur = connection.cursor()
        cur.execute("SELECT * FROM createPokemon")
        connection = sqlite3.connect("database.db")
        show = cur.fetchall();
        cur.execute("SELECT name FROM createPokemon")
        connection = sqlite3.connect("database.db")
        names = cur.fetchall();

        # function render_template() renders jinja2 file "create.j2" from frontend/temnpkates folder. 
        return render_template("create.j2", data = data, show = show,created_names= names  )
@app.route("/delete_create/<string:name>")
def delete_created_Pokemon(name):

    #Delete pokemon
    query = "DELETE FROM createPokemon WHERE name= ?;"
    connection = sqlite3.connect("database.db")
    cur = connection.cursor()
    cur.execute(query,(name,))
    connection.commit()
    

    return redirect("/Create")

@app.route("/Information")
def information_page():

    # function render_template() renders jinja2 file "infroamtion.j2" from frontend/temnpkates folder. 
    return render_template("information.j2")



# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application on the local development server.
    # when malking changes have to restart program
    #app.run()

    # if chabges are made this restarts serevr to account for changes in code
    app.run(debug = True)
