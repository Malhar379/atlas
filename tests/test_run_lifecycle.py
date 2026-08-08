from unittest.mock import Mock
from core.execution.service import update_run_status
from core.execution.lifecycle import transition_run
from core.execution.status import RunStatus
import pytest


def test_created_to_queued():
    result = transition_run(
        RunStatus.CREATED,
        RunStatus.QUEUED,
    )

    assert result == RunStatus.QUEUED


def test_queued_to_running():
    result = transition_run(
        RunStatus.QUEUED,
        RunStatus.RUNNING,
    )

    assert result == RunStatus.RUNNING


def test_running_to_completed():
    result = transition_run(
        RunStatus.RUNNING,
        RunStatus.COMPLETED,
    )

    assert result == RunStatus.COMPLETED


def test_invalid_transition():
    with pytest.raises(ValueError):
        transition_run(
            RunStatus.COMPLETED,
            RunStatus.RUNNING,
        )

def test_update_run_status():
    run = Mock()
    run.status = "CREATED"

    db = Mock()

    result = update_run_status(
        run,
        RunStatus.QUEUED,
        db,
    )

    assert result.status == "QUEUED"
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(run)