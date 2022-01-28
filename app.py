from distutils.log import debug
from msilib import schema
from turtle import textinput
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://okopxbqcfddbfm:c490fbea49aaa7351485a97719c1665922547ae5b49f62b4eac66c9378df2467@ec2-34-205-46-149.compute-1.amazonaws.com:5432/dceocr7oeju55r"

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Month(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)
    days_in_month = db.Column(db.Integer, nullable=False)
    days_in_previous_month = db.Column(db.Integer, nullable=False)
    start_day = db.Column(db.Integer, nullable=False)

    def __init__(self, name, year, days_in_month, days_in_previous_month, start_day):
        self.name = name
        self.year = year
        self.days_in_month = days_in_month
        self.days_in_previous_month = days_in_previous_month
        self.start_day = start_day

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer, nullable=False)
    month = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)

    def __init__(self, day, month, year, text):
        self.day = day
        self.month = month
        self.year = year
        self.text = text

class MonthSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "year", "days_in_month", "days_in_previous_month", "start_day")
        
month_schema = MonthSchema()
multiple_month_schema = MonthSchema(many=True)

class ReminderSchema(ma.Schema):
    class Meta:
        feilds = ("id", "day", "month", "year", "text")

reminder_schema = ReminderSchema()
multiple_reminder_schema = ReminderSchema(many=True)


@app.route("/month/add", methods=["POST"])
def add_month():
    post_data = request.get_json()
    name = post_data["name"]
    year = post_data["year"]
    days_in_month = post_data["days_in_month"]
    days_in_previous_month = post_data["days_in_previous_month"]
    start_day = post_data["start_day"]

    record = Month(name, year, days_in_month, days_in_previous_month, start_day)
    db.session.add(record)
    # Once added you must commit 
    db.session.commit()

    return jsonify("Month added")

@app.route("/month/get", methods=["GET"])
def get_all_months():
    records = db.sessions.query(Month).all()
    return jsonify(multiple_month_schema.dump(records))

if __name__ == '__main__':
    app.run(debug=True)