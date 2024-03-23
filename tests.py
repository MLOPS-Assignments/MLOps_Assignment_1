import pytest
from backend.predict import app
import json


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def test_predict_endpoint(client):
    test_data = {
           "Team": "Crewmate",
           "Task Completed": 9,
           "Murdered": 0,
           "Imposter Kills": 1,
           "Game Length": "12m 02s",
           "Ejected": "Yes"
    }

    response = client.post('/predict', data=json.dumps(test_data),
                           content_type='application/json')

    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert 'predicted_outcome' in data
