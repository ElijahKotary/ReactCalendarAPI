from ast import Delete
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
        fields = ("id", "day", "month", "year", "text")

reminder_schema = ReminderSchema()
multiple_reminder_schema = ReminderSchema(many=True)


# Month End Points
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

@app.route("/month/add/multiple", methods=["POST"])
def add_multiple_months():
    post_data = request.get_json()

    for month_data in post_data:
        # Loop checking for repeating data next line
        record_check = db.session.query(Month).filter(Month.name == month_data["name"]).filter(Month.year == month_data["year"]).first()

        if record_check is None:
            name = month_data["name"]
            year = month_data["year"]
            days_in_month = month_data["days_in_month"]
            days_in_previous_month = month_data["days_in_previous_month"]
            start_day = month_data["start_day"]

            record = Month(name, year, days_in_month, days_in_previous_month, start_day)
            db.session.add(record)
            db.session.commit()

    return jsonify("Months added")


@app.route("/month/get", methods=["GET"])
def get_all_months():
    records = db.sessions.query(Month).all()
    print(records)
    print("-------")
    print(multiple_month_schema.dump(records))
    return jsonify(multiple_month_schema.dump(records))

@app.route("/month/get/<year>", methods=["GET"])
def get_months_by_year(year):
    records = db.session.query(Month).filter(Month.year == year).all()
    return jsonify(multiple_month_schema.dump(records))


# Reminder End Point
@app.route("/reminder/add", methods=["POST"])
def add_reminder():
    post_data = request.get_json()
    day = post_data["day"]
    month = post_data["month"]
    year = post_data["year"]
    text = post_data["text"]

    record = Reminder(day, month, year, text)
    db.session.add(record)
    db.session.commit()

    return jsonify("Reminder added")

@app.route("/reminder/get", methods=["GET"])
def get_all_reminders():
    records = db.session.query(Reminder).all()
    return jsonify(multiple_reminder_schema.dump(records))

@app.route("/reminder/get/<month>/<year>", methods=["GET"])
def get_reminders_by_month(month,year):
    records = db.session.query(Reminder).filter(Reminder.month == month).filter(Reminder.year == year).all()
    return jsonify(multiple_reminder_schema.dump(records))


# PUT is an updater method
@app.route("/reminder/update/<id>", methods=["PUT"])
def update_reminder(id):
    record= db.session.query(Reminder).filter(Reminder.id == id).first()

    put_data = request.get_json()
    text = put_data.get["text", None]

    if text is not None:
        record.text = text
        db.session.commmit()

    return jsonify("Reminder updated")

@app.route("/reminder/delete/<id>", methods=["DELETE"])
def delete_reminder(id):
    record = db.session.query(Reminder).filter(Reminder.id== id).frist()

    db.session.delete(record)
    db.session.commmit()

    return jsonify ("Remidner deleted")

if __name__ == '__main__':
    app.run(debug=True)