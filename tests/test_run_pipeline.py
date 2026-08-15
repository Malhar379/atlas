from unittest.mock import Mock

from core.execution.service import execute_run
from core.execution.status import RunStatus


def test_run_pipeline():
    # Mock database
    db = Mock()

    # Mock run
    run = Mock()
    run.id = 1
    run.status = RunStatus.QUEUED.value

    # Mock experiment
    experiment = Mock()
    experiment.plugin = "example"
    run.experiment = experiment

    # Mock plugin
    plugin = Mock()
    plugin.execute.return_value = {
        "result": {
            "message": "Example plugin executed successfully",
        },
        "metrics": {
            "accuracy": 0.94,
            "loss": 0.12,
        },
        "artifacts": {
            "model": "artifacts/model.pkl",
        },
    }

    # Make DB return our run
    db.query.return_value.filter.return_value.first.return_value = run

    # Replace plugin registry lookup
    with __import__("pytest").MonkeyPatch.context() as mp:
        mp.setattr(
            "core.execution.service.get_plugin",
            lambda name: plugin,
        )

        result = execute_run(db, run.id)

    # Final state
    assert run.status == RunStatus.COMPLETED.value

    # Execution result
    assert result["run_id"] == 1
    assert result["status"] == RunStatus.COMPLETED.value

    # Plugin actually executed
    plugin.execute.assert_called_once_with({})

    # Result came back from plugin
    assert result["result"]["result"]["message"] == (
        "Example plugin executed successfully"
    )

    assert result["result"]["metrics"]["accuracy"] == 0.94

    assert "artifacts" in result["result"]

    # Database was committed
    assert db.commit.call_count >= 2