from eosapi import EosApi

account_name = "consumer1111"
private_key = "5KWxgG4rPEXzHnRBaiVRCCE6WAfnqkRpTu1uHzJoQRzixqBB1k3"

api = EosApi(rpc_host="https://jungle3.greymass.com")
api.import_key(account_name, private_key)

trx = {
    "actions": [{
        "account": "eosio.token",
        "name": "transfer",
        "authorization": [
            {
                "actor": account_name,
                "permission": "active",
            },
        ],
        "data": {
            "from": account_name,
            "to": "consumer2222",
            "quantity": "0.0001 EOS",
            "memo": "by eosapi",
        },
    }]
}

resp = api.push_transaction(trx)
print(resp)
