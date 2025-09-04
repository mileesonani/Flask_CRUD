# _____________Without SQL________________

from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)

class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), nullable=False)
    Phone = db.Column(db.String(100), nullable=False)
    Gender = db.Column(db.String(10), nullable=False)
    City = db.Column(db.String(50), nullable=False)

    def __repr__(self) -> str:
        return f"Task {self.id}"
    
with app.app_context():
    db.create_all()

@app.route("/", methods=["POST","GET"])
def index():
    if request.method == "POST":
        name = request.form['Name']
        email = request.form['Email']
        phone = request.form['Phone']
        gender = request.form['Gender']
        city = request.form['City']
        new_task = MyTask(
            Name=name,
            Email=email,
            Phone=phone,
            Gender=gender,
            City=city
        )
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"
    else:
        tasks = MyTask.query.order_by(MyTask.id).all()
        return render_template("index.html", tasks=tasks)
    
@app.route("/add", methods=["POST","GET"])
def add():
    return render_template("add.html")
    
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR:{e}"
    
@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id:int):
    task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.Name = request.form['Name']
        task.Email = request.form['Email']
        task.Phone = request.form['Phone']
        task.Gender = request.form['Gender']
        task.City = request.form['City']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"Error:{e}"
    else:
        return render_template('edit.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)