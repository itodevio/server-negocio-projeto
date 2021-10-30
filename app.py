from flask import Flask, jsonify, request
import requests
import json
import os
from datetime import datetime
app = Flask(__name__)

db_url = os.getenv('DB_URL')
db_auth_token = os.getenv('DB_AUTH_TOKEN')
server_id = os.getenv('SERVER_ID')

client_auth_tokens = [
    '758baa7e-4823-4769-80ac-cd277a9adcb2',
    '38178b34-18f7-42d9-9ee1-e3e684a66c4f',
    '531afd3d-de6b-4f2f-8006-ad5c6a7a35fd',
    '0f0423a1-e8a0-4b67-a09e-206c152e71fb',
    '024f0e20-f537-42a9-a466-b8d741a57dae',
]

op_num = 1

operations = []


def logOperation(client_id, operation, value, acnt1, acnt2=None):
    global op_num

    with open("log.txt", "a") as file_object:
        if acnt2:
            file_object.write(
                f'Timestamp:{datetime.now()} - OperationNumber: {op_num} - ClientID: {client_id} - OperationType: {operation} - Account1: {acnt1} - Account2: {acnt2} - Value: {value}\n')
        else:
            file_object.write(
                f'Timestamp:{datetime.now()} - OperationNumber: {op_num} - ClientID: {client_id} - OperationType: {operation} - Account: {acnt1} - Value: {value}\n')
    op_num += 1


@app.route("/deposito/<acnt>/<amt>", methods=["POST"])
def deposito(acnt, amt):
    if request.headers['auth-token'] not in client_auth_tokens or not request.headers['client-id']:
        return jsonify("Forbidden"), 403

    try:
        requests.get(f'{db_url}/getlock/{server_id}/{acnt}',
                     headers={'auth-token': db_auth_token})
        requests.post(f'{db_url}/deposito',
                      json={'account_id': acnt, 'value': amt,
                            'business_id': server_id},
                      headers={'auth_token': db_auth_token, })

        logOperation(request.headers['client-id'], 'Deposito', amt, acnt)
        requests.post(f'{db_url}/unlock', json={'business_id': server_id,
                                                'account_id': acnt}, headers={'auth-token': db_auth_token})
        return {'value': amt, 'account_id': acnt}
    except Exception as err:
        print(err)
        return jsonify({'error': 'Não foi possível realizar a chamada'}), 400


@app.route("/saque/<acnt>/<amt>", methods=["POST"])
def saque(acnt, amt):
    if request.headers['auth-token'] not in client_auth_tokens or not request.headers['client-id']:
        return jsonify("Forbidden"), 403

    try:
        requests.get(f'{db_url}/getlock/{server_id}/{acnt}',
                     headers={'auth-token': db_auth_token})

        requests.post(f'{db_url}/setbalance',
                      json={'account_id': acnt, 'value': int(amt) * -1,
                            'business_id': server_id},
                      headers={'auth-token': db_auth_token})

        logOperation(request.headers['client-id'], 'Saque', amt, acnt)
        requests.post(f'{db_url}/unlock', json={'business_id': server_id,
                                                'account_id': acnt}, headers={'auth-token': db_auth_token})
        return {'value': amt, 'account_id': acnt}
    except Exception as err:
        print(err)
        return jsonify({'error': 'Não foi possível realizar a chamada'}), 400


@app.route("/saldo/<acnt>", methods=["GET"])
def saldo(acnt):
    if request.headers['auth-token'] not in client_auth_tokens or not request.headers['client-id']:
        return jsonify("Forbidden"), 403

    try:
        requests.get(f'{db_url}/getlock/{server_id}/{acnt}',
                     headers={'auth-token': db_auth_token})

        saldo = requests.get(f'{db_url}/getbalance/{server_id}/{acnt}',
                             headers={'auth-token': db_auth_token})

        logOperation(request.headers['client-id'], 'Saldo', 'N/A', acnt)
        requests.post(f'{db_url}/unlock', json={'business_id': server_id,
                                                'account_id': acnt}, headers={'auth-token': db_auth_token})
        return {'account_id': acnt}
    except Exception as err:
        print(err)
        return jsonify({'error': 'Não foi possível realizar a chamada'}), 400


@app.route("/transferencia/<acnt_orig>/<acnt_dest>/<amt>", methods=["POST"])
def transferencia(acnt_orig, acnt_dest, amt):
    if request.headers['auth-token'] not in client_auth_tokens or not request.headers['client-id']:
        return jsonify("Forbidden"), 403

    try:
        requests.get(f'{db_url}/getlock/{server_id}/{acnt_orig}',
                     headers={'auth-token': db_auth_token})
        requests.get(f'{db_url}/getlock/{server_id}/{acnt_dest}',
                     headers={'auth-token': db_auth_token})

        requests.post(f'{db_url}/setbalance',
                      json={'account_id': acnt_orig, 'value': int(amt) * -1,
                            'business_id': server_id},
                      headers={'auth-token': db_auth_token})
        requests.post(f'{db_url}/setbalance',
                      json={'account_id': acnt_dest, 'value': int(amt),
                            'business_id': server_id},
                      headers={'auth-token': db_auth_token})

        requests.post(f'{db_url}/unlock', json={'business_id': server_id,
                                                'account_id': acnt_dest}, headers={'auth-token': db_auth_token})
        requests.post(f'{db_url}/unlock', json={'business_id': server_id,
                                                'account_id': acnt_orig}, headers={'auth-token': db_auth_token})

        logOperation(request.headers['client-id'],
                     'Transferencia', amt, acnt_orig, acnt_dest)
        return {'account_orig': acnt_orig, 'account_dest': acnt_dest, 'value': amt}
    except Exception as err:
        print(err)
        return jsonify({'error': 'Não foi possível realizar a chamada'}), 400


# if __name__ == "__main__":
#     app.run(port='8000')
