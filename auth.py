#!/usr/bin/env python3

import requests

login = input("Enter login (email/phone): ")
password = input("Enter password: ")
code = input("2FA-code (leave empty if disabled): ")
auth_test = requests.get("https://oauth.vk.com/token", params={
    "grant_type": "password",
    "scope": "all",
    "client_id": 2274003,
    "client_secret": "hHbZxrka2uZ6jB1inYsH",
    "2fa_supported": True,
    "username": login,
    "password": password,
    "code": code,
})
response = auth_test.json()

if not response.get("access_token"):
    print("VK error: {}".format(response.get("error_description")))
    exit(1)

access_token = response.get("access_token")
with open("access_token.txt", "w") as f:
    f.write(access_token)
print("Success! Token saved to access_token.txt")
