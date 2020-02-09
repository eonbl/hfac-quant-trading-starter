import config
import requests
import base64
import json


def login(username, password):
    auth_str = username + ':' + password
    login_headers = {'Accept': 'application/json',
                     'Content-Type': 'application/json',
                     'investfly-app-token': config.APP_TOKEN,
                     'Authorization': 'Basic ' + base64.b64encode(auth_str.encode()).decode("utf-8")}
    response = requests.post(url=config.LOGIN_ENDPOINT, headers=login_headers)
    info = json.loads(response.text)
    return info['clientId'], info['clientToken']


def logout(client_id, client_token):
    logout_headers = {'Accept': 'application/json',
                      'Content-Type': 'application/json',
                      'investfly-client-id': client_id,
                      'investfly-client-token': client_token}
    return requests.post(url=config.LOGOUT_ENDPOINT, headers=logout_headers)
