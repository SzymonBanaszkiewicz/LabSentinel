
import pytest

from services.core.state_machine import StateMachine, SystemState


def test_initial_state_is_boot():
    machine = StateMachine()

    assert machine.state == SystemState.BOOT


def test_boot_can_transition_to_disarmed():
    machine = StateMachine()

    machine.transition(SystemState.DISARMED)

    assert machine.state == SystemState.DISARMED


def test_boot_cannot_transition_directly_to_alarm():
    machine = StateMachine()

    with pytest.raises(ValueError):
        machine.transition(SystemState.ALARM)


def test_disarmed_can_transition_to_armed():
    machine = StateMachine()
    machine.transition(SystemState.DISARMED)

    machine.transition(SystemState.ARMED)

    assert machine.state == SystemState.ARMED
