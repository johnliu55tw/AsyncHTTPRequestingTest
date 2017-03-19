#!/usr/bin/env python3

import argparse
from flask import Flask
from flask import request
from flask import jsonify
from time import sleep

import db


app = Flask(__name__)
app.config['DELAY'] = 0.5  # Delay of every API request


@app.route("/")
def index():
    return "Docking API"


@app.route("/users", methods=['GET'])
def getUsersCollection():
    sleep(app.config['DELAY'])
    users = db.getUsers(searchName=request.args.get('name'),
                        searchType=request.args.get('type'))
    return jsonify(users)


@app.route("/users/<string:userId>", methods=['GET'])
def getUser(userId):
    sleep(app.config['DELAY'])
    try:
        return jsonify(db.getUsers(userId=userId))
    except KeyError:
        return (jsonify({"type": "ResourceNotFound",
                         "message": "User ID {} not found".format(userId)}),
                404,
                {"Content-Type": "application/json"})


@app.route("/patients", methods=['GET'])
def getPatientsCollection():
    sleep(app.config['DELAY'])
    patients = db.getPatients(searchName=request.args.get('name'),
                              nurseId=request.args.get('nurseId'))

    return jsonify(patients)


@app.route("/patients/<string:patientId>", methods=['GET'])
def getPatient(patientId):
    sleep(app.config['DELAY'])
    try:
        return jsonify(db.getPatients(patientId=patientId))
    except KeyError:
        return (jsonify(
                    {"type": "ResourceNotFound",
                     "message": "Patient ID {} not found".format(patientId)}),
                404,
                {"Content-Type": "application/json"})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--delay", type=float, default=0.0,
                        help="Specify the delay time for each endpoint.")
    args = parser.parse_args()

    app.config.from_mapping(DEBUG=True,
                            DELAY=args.delay)
    app.run()
