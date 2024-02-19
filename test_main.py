from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app
import pytest

client = TestClient(app)

def mock_get_list_from_gpt(list_type, number_of_items, gender_of_gifts, price_range):
    # Return a mock list similar to what you expect from the real GPT function
    return [
        {"description": "Mocked Gift 1", "price_range": "100-150"},
        {"description": "Mocked Gift 2", "price_range": "50-100"}
    ]

@pytest.fixture(autouse=True)
def mock_gpt_function(mocker):
    # Use pytest-mock or unittest.mock to patch the get_list_from_gpt function
    mocker.patch(
        'gpt_agent.get_list_from_gpt',
        side_effect=mock_get_list_from_gpt
    )

def test_generate_gift_list():
    response = client.post("/generate-gift-list/", json={
        "list_type": "birthday",
        "number_of_items": 2,
        "gender_of_gifts": "for a 12 years old boy",
        "price_range": "50-150"
    })
    assert response.status_code == 200
    assert response.json() == [
        {"description": "Mocked Gift 1", "agent_items": [...]},  # Fill in expected details
        {"description": "Mocked Gift 2", "agent_items": [...]}
    ]

    # Add more assertions as needed to validate the response structure and data
