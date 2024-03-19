from fastapi.testclient import TestClient
from unittest.mock import patch
import pytest
from main import app
# Assuming the FastAPI app from main.py is named 'app'
client = TestClient(app)

# Mock data and functions
mock_gpt_list = {
        "birthday": [
            {"name": "Smartphone", "price_range": "$300-$500"},
            {"name": "Laptop", "price_range": "$500-$700"},
        ]
    }  # Your mock GPT list data
mock_db_response = {...}  # Mock responses for database operations

test_input_data = {
  "list_type": "birthday",
  "number_of_items": 2,
  "gender_of_gifts": "a 15 yeasr old boy that love basketball ",
  "price_range": "100 - 300"
}


@pytest.fixture
def mock_db_connection():
    with patch("main.get_db_connection") as mock_connection:
        yield mock_connection

def test_generate_gift_list_success(mock_db_connection):
    with patch("main.get_list_from_gpt", return_value=mock_gpt_list), \
         patch("main.check_item_exists", return_value=False), \
         patch("main.store_item"):
        response = client.post("/generate-gift-list/", json=test_input_data)
        assert response.status_code == 200
        
        response_json = response.json()
        print("this is the response_json:", len(response_json))
        assert isinstance(response_json, list) 
