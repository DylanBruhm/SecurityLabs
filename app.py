from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3
import hashlib


app = Flask(__name__)
app.secret_key = "pirate_secret"

@app.route("/")
def home():
    return redirect(url_for("login")) 

@app.route("/data")
def data():
    user_input = request.args.get("input")

    if user_input:
        return f"You entered: {user_input}"
    else:
        return "No input provided"
    


    
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        # get what user typed
        password = request.form.get("password")
        username = request.form.get("username")
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        print("here",hashed_password)

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        # run query using variables
        cursor.execute(
        
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, hashed_password)
        )
 
        # get result
        result = cursor.fetchone()
        conn.close()
        
        # check result
        if result:
            session["user"] = username
            return redirect(url_for("ships"))
             #return f"Welcome: {username}"
        else:
           return render_template("login.html", error="Invalid login")
        
    return render_template("login.html")

@app.route("/ships")
def ships():

    if "user" not in session:

        return redirect(url_for("login"))
        
    username = session["user"]

    
    if  username == "pirate":
        return f"SeaShip: Gold: 1000000000"
        print (username,"-------------------------------")


    

    
    else:
        return redirect(url_for("login"))
        #return render_template("login.html", error="Invalid login")



        

if __name__ == "__main__":
    app.run(debug=True)

