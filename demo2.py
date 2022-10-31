import requests
from eosapi import EosApi
from typing import List
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context


class CipherAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ciphers='DEFAULT:@SECLEVEL=2')
        kwargs['ssl_context'] = context
        return super(CipherAdapter, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        context = create_urllib3_context(ciphers='DEFAULT:@SECLEVEL=2')
        kwargs['ssl_context'] = context
        return super(CipherAdapter, self).proxy_manager_for(*args, **kwargs)


http_client = requests.Session()
http_client.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, " \
                                          "like Gecko) Chrome/101.0.4951.54 Safari/537.36 "
http_client.mount('https://public-wax-on.wax.io', CipherAdapter())



account_name = "m45yy.wam"
# token, copied from the browser, https://all-access.wax.io/api/session
token = "i5X0pgw9axxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


eosapi = EosApi(rpc_host="https://wax.pink.gg")


def wax_sign(serialized_trx: str) -> List[str]:
    url = "https://public-wax-on.wax.io/wam/sign"
    post_data = {
        "serializedTransaction": serialized_trx,
        "description": "jwt is insecure",
        "freeBandwidth": True,
        "website": "play.alienworlds.io",
    }
    headers = {"x-access-token": token}
    resp = http_client.post(url, json=post_data, headers=headers)
    resp = resp.json()
    return resp["signatures"]


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
            "to": "gts3c.c.wam",
            "quantity": "0.00010000 WAX",
            "memo": "by eosapi",
        },
    }]
}

trx = eosapi.make_transaction(trx)
serialized_trx = list(trx.pack())

signatures = wax_sign(serialized_trx)
trx.signatures.extend(signatures)
resp = eosapi.push_transaction(trx)
print(resp)
