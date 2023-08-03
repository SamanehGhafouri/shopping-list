"""API requests"""

import requests
import os

URL = os.environ.get('URL')

class APICalls:

    def create_token(email, password):
        body = {
            'email': email,
            'password': password
        }
        response = requests.post(
                        URL + 'api/user/token/',
                        headers={'Content-Type': 'application/json'},
                        json=body)
        token = response.json()
        return token['token']

    def create_user(username, password2, first_name, last_name):
        body = {
            'email': username,
            'password': password2,
            'first_name': first_name,
            'last_name': last_name
        }
        response = requests.post(
            URL + 'api/user/create/',
            headers={'Content-Type': 'application/json'},
            json=body)
        return response

    def create_store(store_name, important_val, token):
        body = {
            'store_name': store_name,
            'important': important_val
            }
        response = requests.post(
                    URL + 'api/store/stores/',
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': 'Token ' + token
                        },
                    json=body)
        return response

    def get_stores(token):
        response = requests.get(
                URL + 'api/store/stores/',
                headers={'Authorization': 'Token ' + token})
        data = response.json()
        return data

    def get_items_of_a_store(store_pk, token):
        payload = {'store_id': store_pk}
        response = requests.get(
            URL + 'api/store/' + f'{store_pk}' + '/items/',
            headers={'Authorization': 'Token ' + token},
            params=payload
        )
        data = response.json()
        return data

    def create_item(store_pk, item_name, token):
        payload = {'store_id': store_pk}
        body = {
            'name': item_name,
            'store': store_pk
            }
        response = requests.post(
            URL + 'api/store/' + f'{store_pk}' + '/items/',
            headers={'Authorization': 'Token ' + token},
            params=payload,
            json=body
        )
        data = response.json()
        return data

    def delete_store_item(store_pk, item_pk, token):
        response = requests.delete(
            URL + 'api/store/'
            + f'{store_pk}' + '/item/' + f'{item_pk}/',
            headers={'Authorization': 'Token ' + token},
            )
        return response.status_code

    def delete_store(store_pk, token):
        response = requests.delete(
            URL + 'api/store/' + f'{store_pk}/',
            headers={'Authorization': 'Token ' + token},
            )
        return response.status_code

    def edit_store(store_pk, store_name, important, token):
        body = {'store_name': store_name, 'important': important}
        response = requests.put(
            URL + 'api/store/' + f'{store_pk}/',
            headers={'Authorization': 'Token ' + token},
            json=body
            )
        data = response.json()
        return data

    def edit_store_item(store_pk, item_pk, item_name, token):
        body = {'name': item_name, 'store': store_pk}
        response = requests.put(
            URL + 'api/store/'
            + f'{store_pk}' + '/item/' + f'{item_pk}/',
            headers={'Authorization': 'Token ' + token},
            json=body
            )
        data = response.json()
        return data

    def get_store_by_id(store_pk, token):
        response = requests.get(
            URL + 'api/store/' + f'{store_pk}/',
            headers={'Authorization': 'Token ' + token},
            )
        data = response.json()
        return data

    def get_item_by_store_id(store_pk, item_pk, token):
        response = requests.get(
            URL + 'api/store/'
            + f'{store_pk}' + '/item/' + f'{item_pk}/',
            headers={'Authorization': 'Token ' + token},
            )
        data = response.json()
        return data
