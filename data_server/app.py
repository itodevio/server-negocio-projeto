from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

operation_number = 1

accounts = {
    1: {
        "balance": 500,
        "is_lock": False,
        "lockedBy": ""
    },
    2: {
        "balance": 123,
        "is_lock": False,
        "lockedBy": ""
    },
    3: {
        "balance": 435,
        "is_lock": False,
        "lockedBy": ""
    },
    4: {
        "balance": 847,
        "is_lock": False,
        "lockedBy": ""
    },
}

business_auth_tokens = [
    "ed0eefc4-80c3-42d2-84fe-9c27b18fa811",
    "26e49e65-f44a-4530-bfcd-15ccaa6b34d2",
    "c6aa1a9d-1f91-4306-b61d-6a2c7ed7ede4",
]


def isAuth(token):
    return token in business_auth_tokens


def logOperation(business_id, operation_type, account_id, value):
    with open("log.txt", "a") as file_object:
        file_object.write(
            f'Timestamp:{datetime.now()} - OperationNumber: {operation_number} - BusinessServerID: {business_id} - OperationType: {operation_type} - Account: {account_id} - Value: {value}\n')


@app.route("/getbalance/<business_id>/<int:account_id>", methods=["GET"])
def getBalance(business_id, account_id):
    global operation_number
    auth_token = request.headers['auth-token']
    if(not auth_token or not isAuth(auth_token)):
        return "Unauthorized", 401

    if(not business_id or not account_id):
        return "business_id and account_id is required", 400

    if(accounts[account_id]["is_lock"] == True and accounts[account_id]['lockedby'] != business_id):
        return "-1", 400

    accounts[account_id]["is_lock"] = True
    response = jsonify(account=account_id,
                       balance=accounts[account_id]["balance"])

    logOperation(business_id, "getBalance", account_id, 0)
    operation_number += 1

    return response, 200


@app.route("/setbalance", methods=["POST"])
def setBalance():
    global operation_number
    auth_token = request.headers['auth-token']
    if(not auth_token or not isAuth(auth_token)):
        return "Unauthorized", 401

    if(not request.json["business_id"] or not request.json["account_id"] or not request.json["value"]):
        return "business_id, account_id and value is required", 400

    business_id = request.json["business_id"]
    account_id = int(request.json["account_id"])
    value = int(request.json["value"])

    if(accounts[account_id]["is_lock"] == True and accounts[account_id]['lockedby'] != business_id):
        return "-1", 400

    accounts[account_id]["is_lock"] = True
    accounts[account_id]["lockedby"] = business_id
    accounts[account_id]["balance"] = accounts[account_id]["balance"] + value
    response = jsonify(account=account_id,
                       balance=accounts[account_id]["balance"])

    logOperation(business_id, "setbalance", account_id, value)
    operation_number += 1

    return response, 200


@app.route("/getlock/<business_id>/<int:account_id>", methods=["GET"])
def getLock(business_id, account_id):
    global operation_number
    auth_token = request.headers['auth-token']
    if(not auth_token or not isAuth(auth_token)):
        return "Unauthorized", 401

    if(not business_id or not account_id):
        return "business_id and account_id is required", 400

    response = (accounts[account_id]["is_lock"] ==
                True and accounts[account_id]['lockedby'] != business_id) and '-1' or '1'
    logOperation(business_id, "getlock", account_id, 0)
    operation_number += 1

    return response, 200


@app.route("/unlock", methods=["POST"])
def unLock():
    global operation_number
    auth_token = request.headers['auth-token']
    if(not auth_token or not isAuth(auth_token)):
        return "Unauthorized", 401

    if(not request.json["business_id"] or not request.json["account_id"]):
        return "business_id and account_id is required", 400

    business_id = request.json["business_id"]
    account_id = int(request.json["account_id"])

    if(accounts[account_id]["lockedBy"] == business_id):
        logOperation(business_id, "unLock", account_id, 0)
        operation_number += 1
        accounts[account_id]["is_lock"] = False
        return '1', 200
    else:
        return "-1", 400


# if __name__ == "__main__":
#     app.run(port='8080')
