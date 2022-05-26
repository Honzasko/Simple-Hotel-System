#!/usr/bin/python

#import libs
from flask import Flask,render_template,request
from datetime import date
from datetime import datetime
from dateutil import parser
import mysql.connector

app = Flask(__name__) #initialize flask

app.config['TEMPLATES_AUTO_RELOAD'] = True #enable auto reloading templates

@app.route("/",methods=["GET","POST"]) #set home page app route
def index():
    if len(request.form) == 0:
        #executes in case if form do not send any data using post method
        return render_template("main.html")
    else:
        if len(request.form["surname"]) > 1 and len(request.form["lastname"]) > 1 and int(request.form["room_num"]) > 0 and int(request.form["room_num"]) < 51: #checks if it do not return null values or in case of room no. is in correct range
            if  request.form["start_date"] == "": #checks if starting date of stay is not null,if not null,then continues
                return "Invalid start date"
            elif request.form["end_date"] == "":#checks if ending date of stay is not null,if not null,then continues
                return "Invalid end date"
            
            #convert dates to correct format
            start_date = datetime.strptime(request.form['start_date'],'%Y-%m-%d')
            end_date = datetime.strptime(request.form['end_date'],'%Y-%m-%d')

            #check if dates are valid,if are valid then continues
            if start_date <= datetime.today():
                return "Invalid date"
            if end_date <= start_date:
                return "Invalid date"
            
            #initiliaze connection
            connection = mysql.connector.connect(user="mysql",password="1234",host="localhost",database="hotel")
            #getting cursor
            cursor = connection.cursor()

            #sql command that return number rows of rows that are not valid with current form data to protect overiding dates
            cursor.execute("SELECT COUNT(*) as count FROM stays WHERE roomnum=%s and end_date >= %s  and start_date <= %s or start_date > %s ;",(request.form["room_num"],request.form["end_date"],request.form["start_date"],request.form["start_date"]))
            result1 = cursor.fetchall() #fetch data from database
            if result1[0][0] > 0: #in case that bumber of rows from previous command is 0 then continues,other close connection and send coresponding error
                connection.close()
                return "Selected room already ocupied"

            #insert data to table in dabatabase
            cursor.execute("insert into stays (surname,lastname,roomnum,start_date,end_date)VALUES(%s,%s,%s,%s,%s)",(request.form["surname"],request.form["lastname"],request.form["room_num"],request.form["start_date"],request.form["end_date"]))
            connection.commit

            #close connection
            connection.close()

            #return that everything is success
            return "Success"
        else:
            #executes in case that one or more fills in form are null or are not valid
            return "One or more fills are empty or not valid"



#start server
app.run(host="0.0.0.0",port=8080)