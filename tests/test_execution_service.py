from unittest.mock import Mock

import pytest

from core.execution.service import execute_run
from core.execution.status import RunStatus


def test_execute_run_success():
    run = Mock()
    run.id = 1
    run.status = RunStatus.QUEUED.value

    plugin = Mock()
    plugin.execute.return_value = {
        "result": {
            "message": "success",
        },
        "metrics": {
            "accuracy": 0.94,
        },
    }

    experiment = Mock()
    experiment.plugin = "example"
    run.experiment = experiment

    db = Mock()

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(
            "core.execution.service.get_plugin",
            lambda name: plugin,
        )

        db.query.return_value.filter.return_value.first.return_value = run

        result = execute_run(db, 1)

    assert run.status == RunStatus.COMPLETED.value
    assert result["run_id"] == 1
    assert result["status"] == RunStatus.COMPLETED.value
    assert result["result"]["result"]["message"] == "success"

    plugin.execute.assert_called_once_with({})
    assert db.commit.call_count >= 2

def test_execute_run_plugin_failure():
    run = Mock()
    run.id = 1
    run.status = RunStatus.QUEUED.value

    experiment = Mock()
    experiment.plugin = "example"
    run.experiment = experiment

    plugin = Mock()
    plugin.execute.side_effect = ValueError("Plugin exploded")

    db = Mock()

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(
            "core.execution.service.get_plugin",
            lambda name: plugin,
        )

        db.query.return_value.filter.return_value.first.return_value = run

        with pytest.raises(ValueError, match="Plugin exploded"):
            execute_run(db, 1)

    assert run.status == RunStatus.FAILED.value
    db.commit.assert_called()