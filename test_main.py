import requests
import unittest
from unittest.mock import patch
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_generate_gift_list_postman():
    # Define a sample user gift list request
    user_gift_list_request = {
        "list_type": "Birthday",
        "number_of_items": 5,
        "gender_of_gifts": "Male",
        "price_range": "$20-$50"
    }

    # Send a POST request to the FastAPI application running on the specified URL
    response = requests.post("http://localhost:8000/generate-gift-list/", json=user_gift_list_request)

    # Check if the request was successful (status code 200)
    assert response.status_code == 200