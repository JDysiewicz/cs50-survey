import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():

    # error checking if a value not given (if JS disabled)
    if not request.form.get("name") or not request.form.get("house") or not request.form.get("position"):
        return render_template("error.html", message="Error")

    # opens csv and writes new info to it, directs to /sheets (below)
    file = open("survey.csv", "a")
    writer = csv.writer(file)
    writer.writerow((request.form.get("name"), request.form.get("house"), request.form.get("position")))
    file.close()
    return redirect("/sheet")


@app.route("/sheet", methods=["GET"])
def get_sheet():

    # reads the csv file to get a list of lists of the entire csv
    file = open("survey.csv", "r")
    reader = csv.reader(file)
    registered = list(reader)
    file.close()
    print(registered)
    return render_template("success.html", registered=registered)
