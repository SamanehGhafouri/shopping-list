"""API requests"""

import requests


def create_token_api(email, password):
    body = {
        'email': email,
        'password': password
    }
    response = requests.post(
                    'http://127.0.0.1:8000/api/user/token/',
                    headers={'Content-Type': 'application/json'},
                    json=body)
    token = response.json()
    return token['token']


def create_user_api(username, password2, first_name, last_name):
    body = {
        'email': username,
        'password': password2,
        'first_name': first_name,
        'last_name': last_name
    }
    response = requests.post(
        'http://127.0.0.1:8000/api/user/create/',
        headers={'Content-Type': 'application/json'},
        json=body)
    return response


def create_store_api(store_name, important_val, token):
    body = {
        'store_name': store_name,
        'important': important_val
        }
    response = requests.post(
                'http://127.0.0.1:8000/api/store/stores/',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': 'Token ' + token
                    },
                json=body)
    return response


def get_stores_api(token):
    response = requests.get(
            'http://127.0.0.1:8000/api/store/stores/',
            headers={'Authorization': 'Token ' + token})
    data = response.json()
    return data


def get_items_of_a_store_api(store_pk, token):
    payload = {'store_id': store_pk}
    response = requests.get(
        'http://127.0.0.1:8000/api/store/' + f'{store_pk}' + '/items/',
        headers={'Authorization': 'Token ' + token},
        params=payload
    )
    data = response.json()
    return data
