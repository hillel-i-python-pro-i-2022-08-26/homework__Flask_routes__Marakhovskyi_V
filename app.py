from flask import Flask, render_template
from faker import Faker
import requests
import json
import csv


app = Flask(__name__, template_folder="templates")


@app.route("/")
def home_page():
    return (
        "<h2>This is a homepage. "
        "For completing other task please "
        "enter additional info after slash</h2>"
    )


@app.route("/requirements/<name>")
def read_txt(name):

    return render_template(name)


@app.route("/generate_users/")
def generate_users_default():
    fake = Faker()
    Faker.seed(0)
    return "".join(
        f'<p>{fake.first_name() + " " + fake.ascii_email()}</p>'
        for _ in range(100)
    )


@app.route("/generate_users/<int:num>")
def generate_users(num: int):
    fake = Faker()
    Faker.seed(0)
    return "".join(
        f'<p>{fake.first_name() + " " + fake.ascii_email()}</p>'
        for _ in range(num)
    )


@app.route("/space/")
def calculate_astronauts():
    url = "http://api.open-notify.org/astros.json"
    response = requests.get(url)
    content = response.text
    deserialized_content = json.loads(content)
    return (
        f"<h3>Total number of astronauts is: " 
        f'{deserialized_content["number"]}'f'</h3>'
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
        average_height_cm = \
            (total_height / people_quantity) * constant_inches_to_cm
        average_weight_kg = \
            (total_weight / people_quantity) * constant_pounds_to_kg
    return (
        f"<h3>1. Average height: {int(average_height_cm)} CM.</h3>"
        f"<h3>2. Average weight: {int(average_weight_kg)} KG.</h3>"
    )


if __name__ == "__main__":
    app.run(debug=True)
