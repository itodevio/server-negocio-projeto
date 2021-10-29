from flask import Flask, jsonify, request
import requests
import json
import os

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


@app.route("/deposito/<acnt>/<amt>", methods=["POST"])
def deposito(acnt, amt):
    if request.headers['auth-token'] not in client_auth_tokens:
        return jsonify("Forbidden"), 403

    try:
        data = requests.post(f'{db_url}/deposito',
                             json={'acnt': acnt, 'amt': amt},
                             headers={'auth_token': db_auth_token, 'server-id': server_id})

        return jsonify("OK")
    except Exception as err:
        print(err)
        return jsonify("É necessário informar o value"), 400


@app.route("/saque/<acnt>/<amt>", methods=["POST"])
def saque(acnt, amt):
    if request.headers['auth-token'] not in client_auth_tokens:
        return jsonify("Forbidden"), 403

    try:
        data = requests.post(f'{db_url}/saque',
                             json={'acnt': acnt, 'amt': amt},
                             headers={'auth-token': db_auth_token, 'server-id': server_id})

        return jsonify("OK")
    except Exception as err:
        print(err)
        return jsonify("É necessário informar o value"), 400


@app.route("/saldo/<acnt>", methods=["GET"])
def saldo(acnt):
    if request.headers['auth-token'] not in client_auth_tokens:
        return jsonify("Forbidden"), 403

    try:
        data = requests.get(f'{db_url}/saldo/{acnt}',
                            headers={'auth-token': db_auth_token, 'server-id': server_id})
        res = data.json()
        return str(res['saldo'])
    except Exception as err:
        print(err)
        return jsonify("É necessário informar o value"), 400


@app.route("/transferencia/<acnt_orig>/<acnt_dest>/<amt>", methods=["POST"])
def transferencia(acnt_orig, acnt_dest, amt):
    if request.headers['auth-token'] not in client_auth_tokens:
        return jsonify("Forbidden"), 403

    try:
        data = requests.post(f'{db_url}/transferencia',
                             json={'acnt_orig': acnt_orig,
                                   'acnt_dest': acnt_dest, 'amt': amt},
                             headers={'auth-token': db_auth_token, 'server-id': server_id})

        return jsonify("OK")
    except Exception as err:
        print(err)
        return jsonify("É necessário informar o value"), 400
