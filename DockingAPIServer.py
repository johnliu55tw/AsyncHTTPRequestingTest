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
                        searchRole=request.args.get('role'))
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


@app.route("/customers", methods=['GET'])
def getCustomersCollection():
    sleep(app.config['DELAY'])
    customers = db.getCustomers(searchName=request.args.get('name'),
                                salesId=request.args.get('salesId'))

    return jsonify(customers)


@app.route("/customers/<string:customerId>", methods=['GET'])
def getCustomer(customerId):
    sleep(app.config['DELAY'])
    try:
        return jsonify(db.getCustomers(customerId=customerId))
    except KeyError:
        return (jsonify(
                    {"type": "ResourceNotFound",
                     "message": "Customer ID {} not found".format(
                         customerId)}),
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
