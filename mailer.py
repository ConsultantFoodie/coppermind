from os import environ as env
import requests

def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v3/{}/messages".format(env['MAILGUN_DOMAIN']),
        auth=("api", env['MAILGUN_API_KEY']),
        data={"from": "Excited User <mailgun@{}>".format(env['MAILGUN_DOMAIN']),
              "to": ["hardikti@gmail.com"],
              "subject": "Hello",
              "text": "Testing some Mailgun awesomness!"})