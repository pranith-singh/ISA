from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os, urllib

app = Flask(__name__)

# Read values from Azure App Service environment variables
server = os.environ.get("AZURE_SQL_SERVER")
database = os.environ.get("AZURE_SQL_DATABASE")
username = os.environ.get("AZURE_SQL_USER")
password = os.environ.get("AZURE_SQL_PASSWORD")
port = os.environ.get("AZURE_SQL_PORT", "1433")

# URL encode the password (important if it has special characters like $ or !)
password = urllib.parse.quote_plus(password)

# Build the connection string
db_url = f"mssql+pyodbc://{username}:{password}@{server}:{port}/{database}?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no"

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Table definition
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    message = db.Column(db.Text)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        entry = Contact(
            name=request.form["name"],
            email=request.form["email"],
            message=request.form["message"]
        )
        db.session.add(entry)
        db.session.commit()
        return redirect("/")
    return '''
        <h2>Contact Us</h2>
        <form method="POST">
            Name: <input type="text" name="name"><br>
            Email: <input type="text" name="email"><br>
            Message: <textarea name="message"></textarea><br>
            <button type="submit">Send</button>
        </form>
    '''

@app.route("/initdb")
def initdb():
    db.create_all()
    return "Database initialized!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
