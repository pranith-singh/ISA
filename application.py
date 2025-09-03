from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Direct connection to your Azure SQL DB
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "mssql+pyodbc://user11:Pranith29402941"
    "@thakur3543.database.windows.net:1433/prs"
    "?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

# Initialize DB (run this once)
@app.route("/initdb")
def initdb():
    db.create_all()
    return "Database initialized!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
