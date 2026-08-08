from core.execution.status import RunStatus


VALID_TRANSITIONS = {
    RunStatus.CREATED: {
        RunStatus.QUEUED,
        RunStatus.CANCELLED,
    },

    RunStatus.QUEUED: {
        RunStatus.RUNNING,
        RunStatus.CANCELLED,
    },

    RunStatus.RUNNING: {
        RunStatus.COMPLETED,
        RunStatus.FAILED,
        RunStatus.CANCELLED,
    },

    RunStatus.COMPLETED: set(),
    RunStatus.FAILED: set(),
    RunStatus.CANCELLED: set(),
}


def transition_run(
    current_status: RunStatus,
    new_status: RunStatus,
) -> RunStatus:

    allowed_states = VALID_TRANSITIONS.get(current_status, set())

    if new_status not in allowed_states:
        raise ValueError(
            f"Invalid run transition: "
            f"{current_status.value} -> {new_status.value}"
        )

    return new_status