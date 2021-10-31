from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

business_auth_tokens = [
    "ed0eefc4-80c3-42d2-84fe-9c27b18fa811",
    "26e49e65-f44a-4530-bfcd-15ccaa6b34d2",
    "c6aa1a9d-1f91-4306-b61d-6a2c7ed7ede4",
]

operation_number = 1

accounts = {
    1: {
        "balance": 500,
        "is_lock": False,
        "locked_by": ""
    },
    2: {
        "balance": 123,
        "is_lock": False,
        "locked_by": ""
    },
    3: {
        "balance": 435,
        "is_lock": False,
        "locked_by": ""
    },
    4: {
        "balance": 3984,
        "is_lock": False,
        "locked_by": ""
    },
    5: {
        "balance": 1223,
        "is_lock": False,
        "locked_by": ""
    },
    6: {
        "balance": 912,
        "is_lock": False,
        "locked_by": ""
    },
    7: {
        "balance": 431,
        "is_lock": False,
        "locked_by": ""
    },
    8: {
        "balance": 123,
        "is_lock": False,
        "locked_by": ""
    },
    9: {
        "balance": 2149,
        "is_lock": False,
        "locked_by": ""
    },
    10: {
        "balance": 9008,
        "is_lock": False,
        "locked_by": ""
    },
}


def isAuth(token):
    return token in business_auth_tokens


def logOperation(business_id, operation_type, account_id, value):
    global operation_number
    with open("log.txt", "a") as file_object:
        file_object.write(
            f'Timestamp:{datetime.now()} - OperationNumber: {operation_number} - BusinessServerID: {business_id} - OperationType: {operation_type} - Account: {account_id} - Value: {value}\n'
        )
        operation_number = operation_number + 1


@app.route("/getbalance/<business_id>/<int:account_id>", methods=["GET"])
def getBalance(business_id, account_id):
    print("Accounts - getbalance", accounts[1])
    auth_token = request.headers['auth-token']

    if(not auth_token or not isAuth(auth_token)):
        return "Unauthorized", 401

    if(not business_id or not account_id):
        return "business_id and account_id is required", 400

    if(
        accounts[account_id]["is_lock"] == True and
        accounts[account_id]['locked_by'] != business_id
    ):
        return '-1', 400

    accounts[account_id]["is_lock"] = True
    response = jsonify(account=account_id,
                       balance=accounts[account_id]["balance"])

    logOperation(business_id, "getBalance", account_id, 0)

    return response, 200


@app.route("/setbalance", methods=["POST"])
def setBalance():
    auth_token = request.headers['auth-token']

    if(not auth_token or not isAuth(auth_token)):
        return "Unauthorized", 401

    if(not request.json["business_id"] or not request.json["account_id"] or not request.json["value"]):
        return "business_id, account_id and value is required", 400

    business_id = request.json["business_id"]
    account_id = int(request.json["account_id"])
    value = int(request.json["value"])

    print("Accounts - setbalance - 1 >>>", accounts[account_id])

    if(accounts[account_id]["is_lock"] == True and accounts[account_id]['locked_by'] != business_id):
        return '-1', 400

    accounts[account_id]["is_lock"] = True
    accounts[account_id]["locked_by"] = business_id
    accounts[account_id]["balance"] = accounts[account_id]["balance"] + value
    print("Accounts - setbalance - 2 >>>", accounts[account_id])
    response = jsonify(account=account_id,
                       balance=accounts[account_id]["balance"])

    logOperation(business_id, "setbalance", account_id, value)

    return response, 200


@app.route("/getlock/<business_id>/<int:account_id>", methods=["GET"])
def getLock(business_id, account_id):
    print("Accounts - getlock", accounts[1])
    auth_token = request.headers['auth-token']

    if(not auth_token or not isAuth(auth_token)):
        return "Unauthorized", 401

    if(not business_id or not account_id):
        return "business_id and account_id is required", 400

    response = (accounts[account_id]["is_lock"] ==
                True and accounts[account_id]['locked_by'] != business_id) and '-1' or '1'
    logOperation(business_id, "getlock", account_id, 0)

    return response, 200


@app.route("/unlock", methods=["POST"])
def unLock():
    auth_token = request.headers['auth-token']
    if(not auth_token or not isAuth(auth_token)):
        return "Unauthorized", 401

    if(not request.json["business_id"] or not request.json["account_id"]):
        return "business_id and account_id is required", 400

    business_id = request.json["business_id"]
    account_id = int(request.json["account_id"])

    print("Accounts - unlock >>>", accounts[account_id])

    if(accounts[account_id]["locked_by"] == business_id):
        logOperation(business_id, "unLock", account_id, 0)
        return '1', 200
    else:
        return '-1', 400
