
from enum import Enum


class SystemState(Enum):
    BOOT = "BOOT"
    DISARMED = "DISARMED"
    ARMED = "ARMED"
    OCCUPIED = "OCCUPIED"
    ALARM = "ALARM"
    LOCKDOWN = "LOCKDOWN"


class SystemEvent(Enum):
    STARTUP_COMPLETE = "STARTUP_COMPLETE"
    ARM = "ARM"
    DISARM = "DISARM"
    PRESENCE_DETECTED = "PRESENCE_DETECTED"
    PRESENCE_CLEARED = "PRESENCE_CLEARED"
    INTRUSION_DETECTED = "INTRUSION_DETECTED"
    EMERGENCY_LOCKDOWN = "EMERGENCY_LOCKDOWN"


ALLOWED_TRANSITIONS = {
    SystemState.BOOT: {SystemState.DISARMED},
    SystemState.DISARMED: {SystemState.ARMED},
    SystemState.ARMED: {
        SystemState.DISARMED,
        SystemState.OCCUPIED,
        SystemState.ALARM,
    },
    SystemState.OCCUPIED: {
        SystemState.DISARMED,
        SystemState.ARMED,
        SystemState.ALARM,
    },
    SystemState.ALARM: {SystemState.LOCKDOWN},
    SystemState.LOCKDOWN: set(),
}


class StateMachine:
    def __init__(self):
        self._state = SystemState.BOOT
        self.history = []

    @property
    def state(self) -> SystemState:
        return self._state

    def transition(self, new_state: SystemState) -> None:
        if new_state not in ALLOWED_TRANSITIONS[self._state]:
            raise ValueError(
                f"Invalid transition: {self._state.value} "
                f"-> {new_state.value}"
            )

        previous_state = self._state
        self._state = new_state
        self.history.append((previous_state, new_state))

    def handle_event(self, event: SystemEvent) -> None:
        event_transitions = {
            (SystemState.BOOT, SystemEvent.STARTUP_COMPLETE):
                SystemState.DISARMED,

            (SystemState.DISARMED, SystemEvent.ARM):
                SystemState.ARMED,

            (SystemState.ARMED, SystemEvent.DISARM):
                SystemState.DISARMED,

            (SystemState.ARMED, SystemEvent.PRESENCE_DETECTED):
                SystemState.OCCUPIED,

            (SystemState.OCCUPIED, SystemEvent.PRESENCE_CLEARED):
                SystemState.ARMED,

            (SystemState.OCCUPIED, SystemEvent.DISARM):
                SystemState.DISARMED,

            (SystemState.ARMED, SystemEvent.INTRUSION_DETECTED):
                SystemState.ALARM,

            (SystemState.OCCUPIED, SystemEvent.INTRUSION_DETECTED):
                SystemState.ALARM,

            (SystemState.ALARM, SystemEvent.EMERGENCY_LOCKDOWN):
                SystemState.LOCKDOWN,
        }

        target_state = event_transitions.get((self._state, event))

        if target_state is None:
            raise ValueError(
                f"Event {event.value} is not allowed "
                f"in state {self._state.value}"
            )

        self.transition(target_state)
