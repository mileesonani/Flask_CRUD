from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
import urllib
import os

app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)

params = urllib.parse.quote_plus(
    f"Driver={os.getenv('DB_DRIVER')};"
    f"Server={os.getenv('DB_SERVER')};"
    f"Database={os.getenv('DB_NAME')};"
    f"Trusted_Connection=yes;"
)

conn_str = f"mssql+pyodbc:///?odbc_connect={params}"
ApiSQLEngine = create_engine(conn_str)

# For SQLite (ORM way)
class User(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), nullable=False)
    Phone = db.Column(db.String(100), nullable=False)
    Gender = db.Column(db.String(10), nullable=False)
    City = db.Column(db.String(50), nullable=False)

@app.route("/", methods=["POST","GET"])
def indexSql():
    conn = ApiSQLEngine.connect()
    # result = conn.execute("SELECT * FROM Employee")
    if request.method == "POST":
        name = request.form['Name']
        email = request.form['Email']
        phone = request.form['Phone']
        gender = request.form['Gender']
        city = request.form['City']
        try:
            conn.execute(text("""
                INSERT INTO DataEmployee (Name, Email, Phone, Gender, City)
                VALUES (:name, :email, :phone, :gender, :city)
            """), {
                "name": name,
                "email": email,
                "phone": phone,
                "gender": gender,
                "city": city
            })
            conn.commit()  # Needed if using SQLAlchemy Core
            return redirect("/")
        except Exception as e:
            print(f"ERROR: {e}")
            return f"ERROR: {e}"
    # Get all users
    result = conn.execute(text("SELECT * FROM DataEmployee"))
    user_list = result.fetchall()
    conn.close()
    return render_template("indexSql.html", users=user_list)
    
@app.route("/add", methods=["POST","GET"])
def add():
    return render_template("addSql.html")
    
@app.route("/delete/<int:id>")
def delete(id:int):
    conn = ApiSQLEngine.connect()
    try:
        conn.execute(text("DELETE FROM DataEmployee WHERE ID = :id"), {"id": id})
        conn.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR: {e}"
    
@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id:int):
    conn = ApiSQLEngine.connect()
    if request.method == "POST":
        name = request.form["Name"]
        email = request.form["Email"]
        phone = request.form["Phone"]
        gender = request.form["Gender"]
        city = request.form["City"]
        try:
            conn.execute(text("""
                UPDATE DataEmployee
                SET Name = :name,
                    Email = :email,
                    Phone = :phone,
                    Gender = :gender,
                    City = :city
                WHERE ID = :id
            """), {
                "id": id,
                "name": name,
                "email": email,
                "phone": phone,
                "gender": gender,
                "city": city
            })
            conn.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR: {e}"
    else:
        result = conn.execute(text("SELECT * FROM DataEmployee WHERE ID = :id"), {"id": id})
        user = result.fetchone()
        conn.close()
        return render_template("editSql.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)