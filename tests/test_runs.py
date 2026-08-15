from unittest.mock import patch


def test_create_run(client):
    experiment_response = client.post(
        "/experiments/",
        json={
            "name": "Run Test Experiment",
            "plugin": "example",
            "config": {
                "epochs": 10,
                "learning_rate": 0.01,
            },
        },
    )

    experiment_id = experiment_response.json()["id"]

    response = client.post(
        "/runs/",
        json={
            "experiment_id": experiment_id,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["experiment_id"] == experiment_id
    assert data["status"] == "CREATED"
    assert data["config"]["epochs"] == 10
    assert data["config"]["learning_rate"] == 0.01

def test_execute_run_queues_task(client):
    experiment_response = client.post(
        "/experiments/",
        json={
            "name": "Execution Test",
            "plugin": "example",
            "config": {
                "epochs": 10,
            },
        },
    )

    experiment_id = experiment_response.json()["id"]

    run_response = client.post(
        "/runs/",
        json={
            "experiment_id": experiment_id,
        },
    )

    run_id = run_response.json()["id"]

    with patch("api.routers.runs.execute_run.delay") as mock_delay:
        response = client.post(f"/runs/{run_id}/execute")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == run_id
    assert data["status"] == "QUEUED"

    mock_delay.assert_called_once_with(run_id)