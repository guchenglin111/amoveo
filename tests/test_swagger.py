from base import ApiUser
from nose.tools import nottest

import json


class SwaggerTest(ApiUser):
    URL = "http://localhost:3012/v1"

    def test_new_keypair(self):
        uri = self.URL + "/keypair"
        response = self.session.get(uri)
        self.assertEqual(response.status_code, 200)

    def new_pubkey(self):
        uri = self.URL + "/keypair"
        response = self.session.get(uri)
        o = response.json()
        return o['public']

    def test_account(self):
        pub = self.new_pubkey()
        uri = self.URL + "/account"
        data = {"pubkey": pub, "amount": 10}
        response = self.session.post(uri, json=data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data, {})

    def test_top(self):
        uri = self.URL + "/top"
        response = self.session.get(uri)
        self.assertEqual(response.status_code, 200)

    def test_add_peer(self):
        uri = self.URL + "/peer"
        # valid
        data = {"ip": "46.101.103.165", "port": 8080}
        response = self.session.post(uri, json=data)
        self.assertEqual(response.status_code, 200)
        # invalid
        data = {"ip": "46.101.103165", "port": 8080}
        response = self.session.post(uri, json=data)
        self.assertEqual(response.status_code, 405)

    def create_account(self, amount):
        pub = self.new_pubkey()
        uri = self.URL + "/account"
        data = {"pubkey": pub, "amount": amount}
        self.session.post(uri, json=data)
        return pub

    def test_spend(self):
        pub = self.create_account(10)
        uri = self.URL + "/spend"
        data = {"pubkey": pub, "amount": 5}
        response = self.session.post(uri, json=data)
        self.assertEqual(response.status_code, 200)

    def load_keypair(self, public, private, brainwallet):
        uri = self.URL + "/load-keypair"
        data = {
            "public": public,
            "private": private,
            "brain-wallet": brainwallet
        }
        self.session.post(uri, json=data)
