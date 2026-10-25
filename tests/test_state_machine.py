
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


def test_disarmed_cannot_transition_directly_to_alarm():
    machine = StateMachine()
    machine.transition(SystemState.DISARMED)

    with pytest.raises(ValueError):
        machine.transition(SystemState.ALARM)


def test_armed_can_transition_to_alarm():
    machine = StateMachine()
    machine.transition(SystemState.DISARMED)
    machine.transition(SystemState.ARMED)
    machine.transition(SystemState.ALARM)

    assert machine.state == SystemState.ALARM


def test_alarm_can_transition_to_lockdown():
    machine = StateMachine()
    machine.transition(SystemState.DISARMED)
    machine.transition(SystemState.ARMED)
    machine.transition(SystemState.ALARM)
    machine.transition(SystemState.LOCKDOWN)

    assert machine.state == SystemState.LOCKDOWN


def test_lockdown_cannot_transition_to_disarmed():
    machine = StateMachine()
    machine.transition(SystemState.DISARMED)
    machine.transition(SystemState.ARMED)
    machine.transition(SystemState.ALARM)
    machine.transition(SystemState.LOCKDOWN)

    with pytest.raises(ValueError):
        machine.transition(SystemState.DISARMED)


def test_invalid_transition_does_not_change_state():
    machine = StateMachine()
    initial_state = machine.state

    with pytest.raises(ValueError):
        machine.transition(SystemState.ALARM)

    assert machine.state == initial_state


from services.core.state_machine import SystemEvent


def test_startup_complete_event():
    machine = StateMachine()
    machine.handle_event(SystemEvent.STARTUP_COMPLETE)

    assert machine.state == SystemState.DISARMED


def test_arm_event():
    machine = StateMachine()
    machine.handle_event(SystemEvent.STARTUP_COMPLETE)
    machine.handle_event(SystemEvent.ARM)

    assert machine.state == SystemState.ARMED


def test_presence_detected_event():
    machine = StateMachine()
    machine.handle_event(SystemEvent.STARTUP_COMPLETE)
    machine.handle_event(SystemEvent.ARM)
    machine.handle_event(SystemEvent.PRESENCE_DETECTED)

    assert machine.state == SystemState.OCCUPIED


def test_intrusion_triggers_alarm():
    machine = StateMachine()
    machine.handle_event(SystemEvent.STARTUP_COMPLETE)
    machine.handle_event(SystemEvent.ARM)
    machine.handle_event(SystemEvent.INTRUSION_DETECTED)

    assert machine.state == SystemState.ALARM


def test_invalid_event_does_not_change_state():
    machine = StateMachine()

    with pytest.raises(ValueError):
        machine.handle_event(SystemEvent.ARM)

    assert machine.state == SystemState.BOOT

def test_transition_history_records_valid_transitions():
    machine = StateMachine()

    machine.transition(SystemState.DISARMED)
    machine.transition(SystemState.ARMED)

    assert machine.history == [
        (SystemState.BOOT, SystemState.DISARMED),
        (SystemState.DISARMED, SystemState.ARMED),
    ]


def test_invalid_transition_does_not_modify_history():
    machine = StateMachine()
    initial_history = machine.history.copy()

    with pytest.raises(ValueError):
        machine.transition(SystemState.ALARM)

    assert machine.state == SystemState.BOOT
    assert machine.history == initial_history


def test_presence_cleared_returns_to_armed():
    machine = StateMachine()

    machine.handle_event(SystemEvent.STARTUP_COMPLETE)
    machine.handle_event(SystemEvent.ARM)
    machine.handle_event(SystemEvent.PRESENCE_DETECTED)
    machine.handle_event(SystemEvent.PRESENCE_CLEARED)

    assert machine.state == SystemState.ARMED
