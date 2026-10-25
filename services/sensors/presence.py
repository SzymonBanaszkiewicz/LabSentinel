import random


class PIRSensor:
    def __init__(
        self,
        failure_probability: float = 0.05,
        disturbance_probability: float = 0.02,
    ):
        self.failure_probability = failure_probability
        self.disturbance_probability = disturbance_probability

    def _read_sensor(
        self
    ) -> bool | None:
        # Symulacja awarii czujnika
        if random.random() < self.failure_probability:
            return None

        # Symulacja nietypowego zdarzenia
        if random.random() < self.disturbance_probability:
            return True;

        # Zwykły pomiar
        presence: bool = False
        if random.random() < 0.1:
            presence = True
        return presence


    def read_presence(self) -> bool | None:
        return self._read_sensor()

class UltrasonicSensor:
    def __init__(
        self,
        failure_probability: float = 0.05,
        disturbance_probability: float = 0.02,
    ):
        self.failure_probability = failure_probability
        self.disturbance_probability = disturbance_probability

    def _read_sensor(
        self,
        minimum: float,
        maximum: float,
        disturbance_min: float,
        disturbance_max: float,
    ) -> float | None:
        # Symulacja awarii czujnika
        if random.random() < self.failure_probability:
            return None

        # Symulacja nietypowego zdarzenia
        if random.random() < self.disturbance_probability:
            return round(
                random.uniform(disturbance_min, disturbance_max), 2
            )

        # Zwykły pomiar
        return round(random.uniform(minimum, maximum), 2)

    def read_distance(self) -> float | None:
        return self._read_sensor(2, 400, 478, 829)
