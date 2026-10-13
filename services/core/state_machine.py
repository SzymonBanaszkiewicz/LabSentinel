
from enum import Enum


class SystemState(Enum):
    BOOT = "BOOT"
    DISARMED = "DISARMED"
    ARMED = "ARMED"
    OCCUPIED = "OCCUPIED"
    ALARM = "ALARM"
    LOCKDOWN = "LOCKDOWN"


class StateMachine:
    def __init__(self):
        self._state = SystemState.BOOT

    @property
    def state(self) -> SystemState:
        return self._state

    def transition(self, new_state: SystemState) -> None:
        allowed_transitions = {
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

        if new_state not in allowed_transitions[self._state]:
            raise ValueError(
                f"Invalid transition: {self._state.value} "
                f"-> {new_state.value}"
            )

        self._state = new_state
