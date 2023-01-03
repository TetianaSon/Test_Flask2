import csv

from marshmallow import validate
from webargs import fields
from webargs.flaskparser import use_kwargs
from flask import Flask, request
from faker import Faker
from db import execute_query
from utils import format_records

app = Flask(__name__)


@app.route('/')
def hi_there():
    return "<p>Hi, there!</p>"


#  View function that returns the contents of a
#  file with installed packages in the current
#  project (requirements.txt)
@app.route('/requirements')
def get_requirements():
    requirements = ''
    with open('requirements.txt', 'rt') as freading:
        requirements = freading.read()
        return requirements


#  view function that returns a list of random students.
@app.route('/random_students')
def get_random_students():
    random_students = ''
    length = int(request.args['length'])
    for i in range(length):
        fake = Faker()
        random_students += '<p>' + fake.name() + '</p>'
    print(random_students)
    return random_students


#  view-function that will return the average height and average
#  weight (in cm and kg, respectively) for students from the file hw.csv
@app.route('/avr_data')
def get_avg_data():
    avg_height_sum = 0
    avg_height = 0
    avg_weight_sum = 0
    avg_weight = 0
    inches_to_cm_ratio = 2.54
    pound_to_kg_ratio = 2.2046
    with open('hw.csv', 'rt') as freading:
        csvreading = csv.DictReader(freading)
        data = [row for row in csvreading]
    for i in range(1, len(data)):
        avg_height_sum += float(data[i][' "Height(Inches)"'])
        avg_weight_sum += float(data[i][' "Weight(Pounds)"'])
    avg_height = (avg_height_sum / len(data)) * inches_to_cm_ratio
    avg_weight = (avg_weight_sum / len(data)) / pound_to_kg_ratio
    return "<p>Average height(cm): " + '{:.3f}'.format(avg_height) + \
        "</p>" + "<p>Average weight(kg): " + '{:.3f}'.format(avg_weight) + "</p>"


@app.route('/customers')
@use_kwargs(
    {
        "first_name": fields.Str(
            required=False,
            load_default=None,
            validate=[validate.Regexp('^[0-9]*')]
        ),
        "last_name": fields.Str(
            required=False,
            load_default=None,
            validate=[validate.Regexp('^[0-9]*')]
        ),
    },
    location="query",
)
def get_customers(first_name, last_name):
    query = 'select * from customers'
    fields = {}
    if first_name:
        fields["FirstName"] = first_name

    if last_name:
        fields["LastName"] = last_name

    if fields:
        query += ' WHERE ' + ' AND '.join(f'{k}="{v}"' for k, v in fields.items())
    records = execute_query(query)
    result = format_records(records)
    return result


app.run(port=5500, debug=True)
