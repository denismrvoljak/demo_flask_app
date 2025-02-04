# Imports
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create app
app = Flask(__name__)

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db = SQLAlchemy(app)


# Data Model
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Task {self.id}"


# Initialize database tables
with app.app_context():
    db.create_all()


# Routes
@app.route("/", methods=["POST", "GET"])
def index():
    try:
        if request.method == "POST":
            current_task = request.form["content"]
            new_task = MyTask(content=current_task)
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")

        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template("index.html", tasks=tasks)
    except Exception as e:
        print(f"Error in index route: {e}")
        return f"An error occurred: {e}", 500


@app.route("/delete/<int:id>")
def delete(id):
    try:
        task = MyTask.query.get_or_404(id)
        db.session.delete(task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(f"Error in delete route: {e}")
        return f"An error occurred: {e}", 500


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    try:
        task = MyTask.query.get_or_404(id)
        if request.method == "POST":
            task.content = request.form["content"]
            db.session.commit()
            return redirect("/")
        return render_template("edit.html", task=task)
    except Exception as e:
        print(f"Error in edit route: {e}")
        return f"An error occurred: {e}", 500


if __name__ == "__main__":
    app.run(debug=True)
