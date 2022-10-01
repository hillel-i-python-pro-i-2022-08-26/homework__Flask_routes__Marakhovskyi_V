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

contact_name = "contact_name"

phone_value = "phone_value"


@app.route("/phones/create")
@use_args(
    {contact_name: fields.Str(required=True), phone_value: fields.Int(required=True)},
    location="query",
)
def phone__create(args):
    with DBConnection() as connection:
        with connection:
            connection.execute(
                "INSERT INTO phones (contact_name, phone_value) VALUES (:contact_name, :phone_value);",
                {contact_name: args[contact_name], phone_value: args[phone_value]},
            )

    return "<h3>New entry was added to phone book!</h3>"


@app.route("/phones/read-all")
def phones__read_all():
    with DBConnection() as connection:
        phones = connection.execute("SELECT * FROM phones;").fetchall()

    return "<br>".join(
        [
            f'{phone["phone_id"]}: {phone[contact_name]} - {phone[phone_value]}'
            for phone in phones
        ]
    )


@app.route("/phones/read/<int:phone_id>")
def phones__read(phone_id: int):
    with DBConnection() as connection:
        user = connection.execute(
            "SELECT * " "FROM phones " "WHERE (phone_id=:phone_id);",
            {
                "phone_id": phone_id,
            },
        ).fetchone()

    return f'{user["phone_id"]}: {user[contact_name]} - {user[phone_value]}'


@app.route("/phones/update/<int:phone_id>")
@use_args({phone_value: fields.Int(), contact_name: fields.Str()}, location="query")
def phonecontacts__update(
    args,
    phone_id: int,
):
    with DBConnection() as connection:
        with connection:
            contact_name = args.get("contact_name")
            phone_value = args.get("phone_value")
            if contact_name is None and phone_value is None:
                return Response(
                    "<h3>Need to provide at least one argument</h3>",
                    status=400,
                )

            args_for_request = []
            if contact_name is not None:
                args_for_request.append("contact_name=:contact_name")
            if phone_value is not None:
                args_for_request.append("phone_value=:phone_value")

            args_2 = ", ".join(args_for_request)

            connection.execute(
                "UPDATE phones " f"SET {args_2} " "WHERE phone_id=:phone_id;",
                {
                    "phone_id": phone_id,
                    "phone_value": phone_value,
                    "contact_name": contact_name,
                },
            )

    return "<h3>Phone book was successfully updated</h3>"


@app.route("/phones/delete/<int:phone_id>")
def phonecontacts__delete(phone_id):
    with DBConnection() as connection:
        with connection:
            connection.execute(
                "DELETE " "FROM phones " "WHERE (phone_id=:phone_id);",
                {
                    "phone_id": phone_id,
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
        f"<p>{fake.first_name()} {fake.ascii_email()}</p>" for _ in range(100)
    )


@app.route("/generate-users/<int:num>")
def generate_users(num: int):
    fake = Faker()
    Faker.seed(0)
    return "".join(
        f"<p>{fake.first_name()} {fake.ascii_email()}</p>" for _ in range(num)
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
