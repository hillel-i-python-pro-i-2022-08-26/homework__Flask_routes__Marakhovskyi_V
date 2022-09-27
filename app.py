from flask import Flask, Response
from faker import Faker
import requests
import json
import csv
from webargs import fields
from webargs.flaskparser import use_args

from application.services.create_table import create_table
from application.services.db_connection import DBConnection


app = Flask(__name__, template_folder="templates")


@app.route("/phones/create")
@use_args(
    {"ContactName": fields.Str(required=True), "PhoneValue": fields.Int(required=True)},
    location="query",
)
def phone__create(args):
    with DBConnection() as connection:
        with connection:
            connection.execute(
                "INSERT INTO phones (ContactName, PhoneValue) VALUES (:ContactName, :PhoneValue);",
                {"ContactName": args["ContactName"], "PhoneValue": args["PhoneValue"]},
            )

    return "<h3>New entry was added to phone book!</h3>"


@app.route("/phones/read-all")
def phones__read_all():
    with DBConnection() as connection:
        phones = connection.execute("SELECT * FROM phones;").fetchall()

    return "<br>".join(
        [
            f'{phone["PhoneID"]}: {phone["ContactName"]} - {phone["PhoneValue"]}'
            for phone in phones
        ]
    )


@app.route("/phones/read/<int:PhoneID>")
def phones__read(PhoneID: int):
    with DBConnection() as connection:
        user = connection.execute(
            "SELECT * " "FROM phones " "WHERE (PhoneID=:PhoneID);",
            {
                "PhoneID": PhoneID,
            },
        ).fetchone()

    return f'{user["PhoneID"]}: {user["ContactName"]} - {user["PhoneValue"]}'


@app.route("/phones/update/<int:PhoneID>")
@use_args({"PhoneValue": fields.Int(), "ContactName": fields.Str()}, location="query")
def phonecontacts__update(
    args,
    PhoneID: int,
):
    with DBConnection() as connection:
        with connection:
            ContactName = args.get("ContactName")
            PhoneValue = args.get("PhoneValue")
            if ContactName is None and PhoneValue is None:
                return Response(
                    "<h3>Need to provide at least one argument</h3>",
                    status=400,
                )

            args_for_request = []
            if ContactName is not None:
                args_for_request.append("ContactName=:ContactName")
            if PhoneValue is not None:
                args_for_request.append("PhoneValue=:PhoneValue")

            args_2 = ", ".join(args_for_request)

            connection.execute(
                "UPDATE phones " f"SET {args_2} " "WHERE PhoneID=:PhoneID;",
                {
                    "PhoneID": PhoneID,
                    "PhoneValue": PhoneValue,
                    "ContactName": ContactName,
                },
            )

    return "<h3>Phone book was successfully updated</h3>"


@app.route("/phones/delete/<int:PhoneID>")
def phonecontacts__delete(PhoneID):
    with DBConnection() as connection:
        with connection:
            connection.execute(
                "DELETE " "FROM phones " "WHERE (PhoneID=:PhoneID);",
                {
                    "PhoneID": PhoneID,
                },
            )

    return "<h3>Selected contact was successfully deleted from phone book</h3>"


@app.route("/")
def home_page():
    return (
        "<h2>This is a homepage. "
        "For completing other task please "
        "enter additional info after slash</h2>"
    )


@app.route("/requirements/")
def read_txt():
    with open("templates/something.txt") as file:
        return "".join(f"<p>{line}</p>" for line in file.read().split("\n"))


@app.route("/generate-users/")
def generate_users_default():
    fake = Faker()
    Faker.seed(0)
    return "".join(
        f'<p>{fake.first_name() + " " + fake.ascii_email()}</p>' for _ in range(100)
    )


@app.route("/generate-users/<int:num>")
def generate_users(num: int):
    fake = Faker()
    Faker.seed(0)
    return "".join(
        f'<p>{fake.first_name() + " " + fake.ascii_email()}</p>' for _ in range(num)
    )


@app.route("/space/")
def calculate_astronauts():
    url = "http://api.open-notify.org/astros.json"
    response = requests.get(url)
    content = response.text
    deserialized_content = json.loads(content)
    return (
        f"<h3>Total number of astronauts is: "
        f'{deserialized_content["number"]}'
        f"</h3>"
    )


@app.route("/mean/")
def calculate_params():
    constant_inches_to_cm = 2.54
    constant_pounds_to_kg = 0.453592
    with open("people_data.csv", "rt", newline="") as csvfile:
        total_height, total_weight, people_quantity = 0, 0, 0
        reader = csv.DictReader(csvfile)
        for row in reader:
            total_height += float(list(row.values())[1])
            total_weight += float(list(row.values())[2])
            people_quantity += 1
        average_height_cm = (total_height / people_quantity) * constant_inches_to_cm
        average_weight_kg = (total_weight / people_quantity) * constant_pounds_to_kg
    return (
        f"<h3>1. Average height: {int(average_height_cm)} CM.</h3>"
        f"<h3>2. Average weight: {int(average_weight_kg)} KG.</h3>"
    )


create_table()

if __name__ == "__main__":
    app.run(debug=True)
