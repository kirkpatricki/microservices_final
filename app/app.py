from flask import Flask, request, render_template, jsonify
from datetime import date
import json

from stats.service import StatsService
from stats.models import Schema

app = Flask(__name__)
USER_ID=0

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Reqested-With"
    response.headers['Access-Control-Allow-Methods'] = "POST, GET, PUT, DELETE, OPTIONS"
    return response

@app.route("/")
def index():
    """
    Currently not fully implemented.
    Once implemented, will show information about the page
    And give option to sign in
    """
    return render_template("index.html", active="HOME")

@app.route("/my_dashboard")
def my_dashboard():
    """
    Currently not fully implemented.
    Once implemented, will redirect to modify service
    for user to add, update, remove job application info.
    """
    response_types_raw = StatsService().get_response_types()
    response_type_dict = {}
    for row in response_types_raw:
        response_type_dict[row['id']] = row['type']
    return render_template(
        "my_dashboard.html",
        apps=StatsService().get_applications(0),
        response_types=response_type_dict,
        user_id=USER_ID
    )

@app.route("/dashboards")
def dashboards():
    """
    Currently not implemeneted.
    Once implemented, will redirect to set of dashboards
    the user is subscribed to.
    """
    return render_template("index.html", active="DASHBOARDS")

@app.route("/delete/<id>", methods=["POST"])
def delete_application(id):
    response = StatsService().delete(id)
    print(response)
    return response

@app.route("/add/<int:user_id>", methods=["POST"])
def add_application(user_id):
    req = request.get_json()
    company_name = req['company_name']
    date_applied = req['date_applied'] if req['date_applied'] != '' else 'NULL'
    date_response = req['date_response'] if req['date_response'] != '' else 'NULL'
    response_type = req['response_type'] if req['response_type'] != '' else 'NULL'
    StatsService().create({
        'user_id': user_id,
        'company_name': company_name,
        'date_applied': date_applied,
        'date_response': date_response,
        'response_type': response_type
    })
    return '', 200

if __name__ == "__main__":
    Schema()
    # for i in range(10):
    #     user_params = {
    #         "user_id": 0,
    #         "company_name": f"sample_company_{i}",
    #         "date_applied": date.today().isoformat(),
    #         "date_response": "NULL",
    #         "response_type": "NULL",
    #     }
    #     with app.app_context():
    #         r = StatsService().create(jsonify(user_params).get_json())
    #         print(r)
    app.run(host='0.0.0.0', debug=True)
