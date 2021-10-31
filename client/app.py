import asyncio
import aiohttp
import time
import random

# bank_api = "http://35.224.105.248"
bank_api = "http://localhost:5000"

accounts = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

client_auth_tokens = [
    '758baa7e-4823-4769-80ac-cd277a9adcb2',
    '38178b34-18f7-42d9-9ee1-e3e684a66c4f',
    '531afd3d-de6b-4f2f-8006-ad5c6a7a35fd',
    '0f0423a1-e8a0-4b67-a09e-206c152e71fb',
    '024f0e20-f537-42a9-a466-b8d741a57dae',
    'banana',
    'wrong-auth-token'
]

clients_id = ['1', '2', '3', '4', '5']


# async def doGetBalance(session):
#     try:
#         auth = random.choice(client_auth_tokens)
#         client = random.choice(clients_id)
#         headers = {
#             "auth-token": auth, "client-id": client}
#         async with session.get(f'{bank_api}/saldo/{random.choice(accounts)}', headers=headers) as response:
#             resp = await response.read()
#             print("Successfully doGetBalance response: {}.".format(resp))
#     except Exception as e:
#         print("Unable to doGetBalance due to {}.".format(e))


# async def doDeposit(session):
#     try:
#         headers = {
#             "auth-token": random.choice(client_auth_tokens), "client-id": random.choice(clients_id)}
#         async with session.post(f'{bank_api}/deposito/{random.choice(accounts)}/{random.randint(50, 425)}', headers=headers) as response:
#             resp = await response.read()
#             print("Successfully doDeposit response: {}.".format(resp))
#     except Exception as e:
#         print("Unable to doDeposit due to {}.".format(e))


# async def doWithdraw(session):
#     try:
#         headers = {
#             "auth-token": random.choice(client_auth_tokens), "client-id": random.choice(clients_id)}
#         async with session.post(f'{bank_api}/saque/{random.choice(accounts)}/{random.randint(50, 425)}', headers=headers) as response:
#             resp = await response.read()
#             print("Successfully doWithdraw response: {}.".format(resp))
#     except Exception as e:
#         print("Unable to doWithdraw due to {}.".format(e))


# async def doTransfer(session):
#     try:
#         headers = {
#             "auth-token": random.choice(client_auth_tokens), "client-id": random.choice(clients_id)}
#         async with session.post(f'{bank_api}/transferencia/{random.choice(accounts)}/{random.choice(accounts)}/{random.randint(50, 425)}', headers=headers) as response:
#             resp = await response.read()
#             print("Successfully doTransfer response: {}.".format(resp))
#     except Exception as e:
#         print("Unable to doTransfer due to {}.".format(e))

async def doGetBalance(session):
    try:
        auth = random.choice(client_auth_tokens)
        client = random.choice(clients_id)
        headers = {
            "auth-token": auth, "client-id": client}
        async with session.get(f'{bank_api}/saldo/{1}', headers=headers) as response:
            resp = await response.read()
            print("Successfully doGetBalance response: {}.".format(resp))
    except Exception as e:
        print("Unable to doGetBalance due to {}.".format(e))


async def doDeposit(session):
    try:
        headers = {
            "auth-token": random.choice(client_auth_tokens), "client-id": random.choice(clients_id)}
        async with session.post(f'{bank_api}/deposito/{1}/{random.randint(50, 425)}', headers=headers) as response:
            resp = await response.read()
            print("Successfully doDeposit response: {}.".format(resp))
    except Exception as e:
        print("Unable to doDeposit due to {}.".format(e))


async def doWithdraw(session):
    try:
        headers = {
            "auth-token": random.choice(client_auth_tokens), "client-id": random.choice(clients_id)}
        async with session.post(f'{bank_api}/saque/{1}/{random.randint(50, 425)}', headers=headers) as response:
            resp = await response.read()
            print("Successfully doWithdraw response: {}.".format(resp))
    except Exception as e:
        print("Unable to doWithdraw due to {}.".format(e))


async def doTransfer(session):
    try:
        headers = {
            "auth-token": random.choice(client_auth_tokens), "client-id": random.choice(clients_id)}
        async with session.post(f'{bank_api}/transferencia/{1}/{2}/{random.randint(50, 425)}', headers=headers) as response:
            resp = await response.read()
            print("Successfully doTransfer response: {}.".format(resp))
    except Exception as e:
        print("Unable to doTransfer due to {}.".format(e))


async def main():
    async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(
            * [doGetBalance(session) for _ in accounts],
            * [doDeposit(session) for _ in accounts],
            * [doWithdraw(session) for _ in accounts],
            * [doTransfer(session) for _ in accounts]
        )
    print("Finalized all. Return is a list of len {} outputs.".format(len(ret)))


start = time.time()
asyncio.run(main())
end = time.time()

print("Took {} seconds to pull.".format(end - start))
