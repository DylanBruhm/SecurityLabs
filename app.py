from flask import Flask, request, render_template, redirect, url_for, session
from datetime import datetime, timedelta
import sqlite3
import hashlib
import os
import time

app = Flask(__name__)
app.secret_key = "pirate_secret"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "users.db")

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

        # current time 
        date = datetime.now()
        formatted_time = date.strftime("%Y-%m-%d %H:%M")
        ten_mins_ago = date - timedelta(minutes=10)
        attempts = 0
        brute_force_warning = 5

        local_ip = request.remote_addr
        password = request.form.get("password")
        username = request.form.get("username")

        


        hashed_password = hashlib.sha256(password.encode()).hexdigest()


        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, hashed_password)
        )

        result = cursor.fetchone()

        
        if result:
            session["user"] = username
            session["role"] = result[3]

            conn.close()


            with open("logins.log", "a") as file:
                file.write(
                    " Time - " + formatted_time +
                    " User - " + username +
                    " - Success - Local IP - " + local_ip + "\n"
                )

            return redirect(url_for("ships"))

        
        else:
            
            with open("logins.log", "a") as file:
                file.write(
                    " Time - " + formatted_time +
                    " User - " + username +
                    " - Failed - Local IP - " + local_ip + "\n"
                )

            count = 0
            # Read log
            with open("logins.log", "r") as file:
                for line in file:
                    parts = line.split()
                    
                    #if no collums continue
                    if not parts:
                        continue
                    # if more then 9 collums contiune
                    if len(parts) < 9:
                        continue
                    # time and date as string
                    log_time_text = parts[2] + " " + parts[3]
                    # take sting and make it into a readable time python can use
                    log_time = datetime.strptime(log_time_text, "%Y-%m-%d %H:%M")

                    # access = login attempt 
                    access = parts[8]
                    # every failed login get saved 
                    if access == "Failed":
                        attempts += 1
                    # show possible brute force attack and then reset attempt not prefect but works for now
                    if access == "Failed" and log_time >= ten_mins_ago and attempts >= brute_force_warning:
                        count += 1
                        print("failed login found", + count)
                        attempts = 0

            return render_template("login.html", error="Invalid login")

    return render_template("login.html")


@app.route("/ships")
def ships():

    if "user" not in session:
        return redirect(url_for("login"))
        
    username = session["user"]
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM ships WHERE owner = ?",
        (username,)
    )

    result = cursor.fetchall()
    conn.close()

    output = ""
    # pritns ship name and inventory
    for row in result:
        output += "Ship: " + row[1] + " | Gold: " + str(row[2]) + "<br>"

    return output

@app.route("/security_dashboard")
def security_dashboard():

    if session.get("role") != "admin":
        return redirect(url_for("login")) 

    with open("logins.log", "r") as file:
            lines = file.readlines()
            last_logs = lines[-5:]

            return render_template("security_dashboard.html", logs=last_logs)






if __name__ == "__main__":
    app.run(debug=True)
    