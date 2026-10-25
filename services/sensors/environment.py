import random


class EnvironmentSensor:
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

    def read_temperature(self) -> float | None:
        return self._read_sensor(-10, 35, 36, 50)

    def read_humidity(self) -> float | None:
        return self._read_sensor(20, 80, 81, 100)

    def read_light(self) -> float | None:
        return self._read_sensor(0, 100, 101, 150)

    def read_sound(self) -> float | None:
        return self._read_sensor(0, 100, 101, 150)

    def read_all(self) -> dict:
        return {
            "temperature": self.read_temperature(),
            "humidity": self.read_humidity(),
            "light": self.read_light(),
            "sound": self.read_sound(),
        }