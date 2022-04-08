import flask
from flask import Flask, render_template, request, redirect
import sqlite3

conn = sqlite3.connect("book.db", check_same_thread=False)
cursor = conn.cursor()

listOfTables= conn.execute("SELECT name from sqlite_master WHERE type='table' AND name='BOOK'").fetchall()
listOfTables1 = conn.execute("SELECT name from sqlite_master WHERE type='table' AND name='USER'").fetchall()

if listOfTables!=[]:
    print("Table Already Exists ! ")
else:
    conn.execute(''' CREATE TABLE BOOK(
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,author TEXT,category TEXT,   
                            price INTEGER, publisher TEXT); ''')
print("Table has created")
if listOfTables1!=[]:
    print("Table Already Exists ! ")
else:
    conn.execute(''' CREATE TABLE USER(
                                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name TEXT, address TEXT, email TEXT, 
                                    phone TEXT, pass TEXT); ''')
print("Table has created")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("/index.html")

@app.route("/adminlogin", methods = ['GET','POST'])
def adminlogin():
    if request.method == 'POST':
        getname = request.form["name"]
        getpass = request.form["pass"]
    try:
        if getname == 'admin' and getpass == "9875":
            return redirect("/addbooks")
        else:
            print("Invalid username and password")
    except Exception as e:
        print(e)
    return render_template("/adminlogin.html")

@app.route("/userlogin", methods = ['GET','POST'])
def userlogin():
    if request.method == 'POST':
        getemail = request.form['email']
        getpass = request.form['pass']
        print(getemail)
        print(getpass)
    
    try:
        query = "SELECT * FROM USER WHERE email='"+getemail+"' AND pass='"+getpass+"'"
        cursor.execute(query)
        result = cursor.fetchall()
        print(result)
        if len(result) == 0:
            print("Invalid USER")
        else:
            return redirect("dashboard")

    except Exception as e:
            print(e)

    return render_template("/userlogin.html")

@app.route("/dashboard", methods = ['GET','POST'])
def dashboard():
    return render_template("/dashboard.html")


@app.route("/register", methods = ['GET','POST'])
def register():

    if request.method == 'POST':
        getname = request.form['name']
        getaddress = request.form['address']
        getemail = request.form['email']
        getphone = request.form['phone']
        getpass = request.form['pass']

        print(getname)
        print(getaddress)
        print(getemail)
        print(getphone)
        print(getpass)

    try:
        query = cursor.execute("INSERT INTO USER(name,address,email,phone,pass)VALUES('"+getname+"','"+getaddress+"','"+getemail+"','"+getphone+"','"+getpass+"')")
        print(query)
        conn.commit()
        return redirect("/userlogin")
    except Exception as e:
        print(e)

    return render_template("/register.html")

@app.route("/addbooks", methods = ['GET','POST'])
def addbooks():
    if request.method == 'POST':
        getname = request.form['name']
        getauthor = request.form['author']
        getcategory = request.form['category']
        getprice = request.form['price']
        getpublisher = request.form['publisher']

        print(getname)
        print(getauthor)
        print(getcategory)
        print(getprice)
        print(getpublisher)

    try:
        query = cursor.execute("INSERT INTO BOOK(name,author,category,price,publisher)VALUES('"+getname+"','"+getauthor+"','"+getcategory+"','"+getprice+"','"+getpublisher+"')")
        print(query)
        conn.commit()
        return redirect("/viewall")
    except Exception as e:
        print(e)

    return render_template("/addbooks.html")


@app.route("/search", methods =['GET','POST'])
def search():
    if request.method == "POST":
        getname = request.form["name"]
        print(getname)
        try:
            query = "SELECT * FROM BOOK WHERE name='"+getname+"'"
            print(query)
            cursor.execute(query)
            print("SUCCESSFULLY SELECTED!")
            result = cursor.fetchall()
            print(result)
            if len(result) == 0:
                print("Invalid Book Name")
            else:
                return render_template("search.html", book=result, status = True)

        except Exception as e:
            print(e)

    return render_template("search.html", book=[], status = False)

@app.route("/usersearch", methods =['GET','POST'])
def usersearch():
    if request.method == "POST":
        getname = request.form["name"]
        print(getname)
        try:
            query = "SELECT * FROM BOOK WHERE name='"+getname+"'"
            print(query)
            cursor.execute(query)
            print("SUCCESSFULLY SELECTED!")
            result = cursor.fetchall()
            print(result)
            if len(result) == 0:
                print("Invalid Book Name")
            else:
                return render_template("usersearch.html", books=result, status = True)

        except Exception as e:
            print(e)

    return render_template("usersearch.html", books=[], status = False)

@app.route("/viewall")
def viewall():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM BOOK")
    result = cursor.fetchall()
    return render_template("viewall.html",books=result)

@app.route("/userviewall")
def userviewall():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM BOOK")
    result = cursor.fetchall()
    return render_template("userviewall.html",books=result)

@app.route("/delete", methods =['GET','POST'])
def delete():
    if request.method == "POST":
        getname = request.form['name']
        print(getname)
        try:
            conn.execute("DELETE FROM BOOK WHERE name='"+getname+"'")
            print("SUCCESSFULLY DELETED!")
            conn.commit()
            return redirect("/viewall")
        except Exception as e:
            print(e)
    return flask.render_template("delete.html")

@app.route("/update", methods =['GET','POST'])
def update():
    if request.method == "POST":
        getname = request.form["name"]
        print(getname)
        try:
            query = "SELECT * FROM BOOK WHERE name='"+getname+"'"
            cursor.execute(query)
            print("SUCCESSFULLY SELECTED!")
            result = cursor.fetchall()
            print(result)
            if len(result) == 0:
                print("Invalid Book Name")
            else:
                return redirect("/viewupdate")

        except Exception as e:
            print(e)

    return render_template("update.html")

@app.route("/viewupdate", methods =['GET','POST'])
def vieupdate():
    if request.method == 'POST':
        getname = request.form['name']
        getauthor = request.form['author']
        getcategory = request.form['category']
        getprice = request.form['price']
        getpublisher = request.form['publisher']

    try:
        cursor.execute("UPDATE BOOK SET name='"+getname+"',author='"+getauthor+"',category='"+getcategory+"',price='"+getprice+"',publisher='"+getpublisher+"'WHERE name='"+getname+"'")
        conn.commit()
        return redirect("/viewall")
    except Exception as e:
        print(e)

    return render_template("/viewupdate.html")

if __name__ == "__main__":
    app.run(debug=True)
