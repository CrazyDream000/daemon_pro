import hashlib
import hmac
import ipaddress
import json
import time

import requests


class RipHelper:

    @staticmethod
    def get_digest_string(headers_dict, data_var):
        to_dig = [
            str(headers_dict["Hmac-User"]) if headers_dict["Hmac-User"] is not None else "",
            str(headers_dict["Hmac-Lookup"]) if headers_dict["Hmac-Lookup"] is not None else "",
            str(headers_dict["Hmac-Time"]) if headers_dict["Hmac-Time"] is not None else "",
            str(data_var) if data_var is not None else ""
        ]
        print(to_dig)
        return "".join(to_dig)


class RipHmac:
    h_key = None
    h_alg = hashlib.sha256

    def __init__(self, key):
        self.h_key = RipEncode.encode_string(key)

    def get_digest(self, message):
        h_byte_array = hmac.new(key=self.h_key, msg=RipEncode.encode_string(message), digestmod=self.h_alg)
        return h_byte_array.digest().hex()


class RipEncode:
    @staticmethod
    def encode_string(value):
        return value.encode("utf-8") if isinstance(value, str) else str(value).encode("utf-8")

    @staticmethod
    def decode_string(value):
        return value.decode("utf-8")


class RipRequest:

    @staticmethod
    def retrieve_my_ip(ip_lookup_server_url="https://supportlink.ch/myip.php"):
        r = requests.get(ip_lookup_server_url)
        return ipaddress.IPv4Address(r.json()["client_ip"])

    @staticmethod
    def json_hmac_request(destination_server_url, api_user, api_key, api_key_number, dictionary_payload,
                          submit_method="GET"):
        payload = json.dumps(dictionary_payload)
        headers = {
            'Authorization': 'HMAC_PER_USER',
            'Hmac-Lookup': str(int(api_key_number)),
            'Hmac-User': str(api_user),
            'Hmac-Value': 'stub_to_be_replaced',
            'Hmac-Time': str(time.time()),
            'Content-Type': 'application/json'
        }
        hmac_dig_string = RipHelper.get_digest_string(headers, RipEncode.encode_string(payload))
        hm = RipHmac(api_key)
        calc_hmac = hm.get_digest(hmac_dig_string)
        headers['Hmac-Value'] = calc_hmac
        response = requests.request(submit_method, destination_server_url, headers=headers, data=payload)
        return response
