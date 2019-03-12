"""
Just for testing the endpoints
"""
import json
import requests

BASE_URL = "http://127.0.0.1:8000/"

ENDPOINT = "api/updates/"


def get_list():
    r = requests.get(BASE_URL + ENDPOINT)
    return r.json()


def create_update():
    new_data = {
        "user": 1,
        "content": "Another new item is here"
    }
    r = requests.post(BASE_URL + ENDPOINT, data=json.dumps(new_data))
    print(r.status_code)
    print(r.json())


def do_object_update():
    new_data = {
        "content": "new updated content"
    }
    r = requests.put(BASE_URL + ENDPOINT + "1/", data=json.dumps(new_data))
    return r.json()


def do_object_delete():
    r = requests.delete(BASE_URL + ENDPOINT + "5/")
    return r.json()


print(get_list())
