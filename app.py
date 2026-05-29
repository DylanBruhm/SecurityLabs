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

    return render_template(
        "ships.html", 
        ships=result

    )

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
    
@app.route("/more_logs", methods=["POST"])  
def more_logs():

    logs_amount = int(request.form["logs_amount"])
    logs_amount += 5

    with open("logins.log", "r") as file:
            lines = file.readlines()
            last_logs = lines[-logs_amount:]

            return render_template("security_dashboard.html", logs=last_logs) 

@app.route("/transfer_gold", methods=["GET","POST"])
def transfer_gold():


    date = datetime.now()
    formatted_time = date.strftime("%Y-%m-%d %H:%M")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if request.method == "POST":

        from_ship = request.form["from_ship"]
        to_ship = request.form["to_ship"]
        amount = request.form["amount"]

        print("tyoed ship:", from_ship)

        cursor.execute(
            "SELECT gold FROM ships WHERE ship = ?",
            (from_ship,)
        )

        
        try:
            sent_gold = int(amount)

        except:
            print("not a number")
            return redirect(url_for("ships")) 
        
        result = cursor.fetchone()
        if result is None:

            print("failed")
            return redirect(url_for("ships"))
        
        gold = result[0]

        new_gold = gold - sent_gold

        if sent_gold <= 0:
            print("invalid amount")
            return redirect(url_for("ships"))
        

        print("herrre",sent_gold, gold, to_ship)
        if gold < sent_gold: 
            print("failed")
            return redirect(url_for("ships"))

        cursor.execute(
            "SELECT gold FROM ships WHERE ship = ?",
            (to_ship,)

        )
        receiver_result = cursor.fetchone()
        if receiver_result is None:

            print("failed")
            return redirect(url_for("ships"))

        receiver_ship = receiver_result[0]
        receiver_new_gold = sent_gold + receiver_ship
        cursor.execute(
            "UPDATE ships SET gold = ? WHERE ship = ?",
            (receiver_new_gold, to_ship)

        )
        cursor.execute(
            "UPDATE ships SET gold = ? WHERE ship = ?",
            (new_gold, from_ship)
        )

        with open("Gold.log", "a") as file:
            file.write(
                    " Time - " + formatted_time +
                    " User - " + from_ship +
                    " Gold: " + str(new_gold) + 
                    " To " + to_ship + 
                    " - Sent Gold: " + str(sent_gold) + " - " +
                      to_ship + " Gold: " + str(receiver_new_gold) +"\n"
                )


        conn.commit()


    return redirect(url_for("ships"))





if __name__ == "__main__":
    app.run(debug=True)
    