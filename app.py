# Imports
from flask import Flask, render_template
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone


# My App
app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dabatase.db"
db = SQLAlchemy(app)


# Data Class ~ Row of data
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Task {self.id}"


# Routes of webpages
@app.route("/")
def index():
    return render_template("index.html")


if __name__ in "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
