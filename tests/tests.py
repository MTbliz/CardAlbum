import requests

BASE = "http://127.0.0.1:5000/"

data = [
    {"title": "testcard", "price": 123, "availability": 100, "type": "creature", "image": None},
]


response = requests.post(BASE + "card", json=data[0])
print(response.json())