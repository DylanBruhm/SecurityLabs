from flask import Flask, request, render_template, redirect, url_for

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
        username = request.form.get("pirate")
        password = request.form.get("shores")

        if username != "pirate" or password != "shores":
            return render_template("login.html", error="Invalid Pirate")
        else:
            return f"Welcome: {username}"

    return render_template("login.html")
        

if __name__ == "__main__":
    app.run(debug=True)

