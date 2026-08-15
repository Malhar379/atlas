def test_create_experiment(client):
    response = client.post(
        "/experiments/",
        json={
            "name": "Test Experiment",
            "plugin": "example",
            "config": {
                "epochs": 10,
                "learning_rate": 0.01,
            },
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Test Experiment"
    assert data["plugin"] == "example"
    assert data["config"]["epochs"] == 10
    assert data["config"]["learning_rate"] == 0.01


def test_get_experiment(client):
    create_response = client.post(
        "/experiments/",
        json={
            "name": "Test Experiment",
            "plugin": "example",
            "config": {"epochs": 10},
        },
    )

    experiment_id = create_response.json()["id"]

    response = client.get(f"/experiments/{experiment_id}")

    assert response.status_code == 200
    assert response.json()["id"] == experiment_id
    assert response.json()["name"] == "Test Experiment"


def test_update_experiment(client):
    create_response = client.post(
        "/experiments/",
        json={
            "name": "Original",
            "plugin": "example",
            "config": {"epochs": 10},
        },
    )

    experiment_id = create_response.json()["id"]

    response = client.put(
        f"/experiments/{experiment_id}",
        json={
            "name": "Updated",
            "plugin": "example",
            "config": {"epochs": 20},
        },
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated"
    assert response.json()["config"]["epochs"] == 20


def test_delete_experiment(client):
    create_response = client.post(
        "/experiments/",
        json={
            "name": "Delete Me",
            "plugin": "example",
            "config": {},
        },
    )

    experiment_id = create_response.json()["id"]

    response = client.delete(f"/experiments/{experiment_id}")

    assert response.status_code == 200

    get_response = client.get(f"/experiments/{experiment_id}")

    assert get_response.status_code == 404


def test_get_missing_experiment(client):
    response = client.get("/experiments/999")

    assert response.status_code == 404