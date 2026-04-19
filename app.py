from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

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
        username = request.form.get("pirate")
        password = request.form.get("shores")

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        # run query using variables
        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        )

        # get result
        result = cursor.fetchone()

        # check result
        if result:
            return f"Welcome: {username}"
        else:
            return render_template("login.html", error="Invalid login")

    return render_template("login.html")
        

if __name__ == "__main__":
    app.run(debug=True)

