from services.sensors.presence import PIRSensor, UltrasonicSensor


class PresenceDetector:
    def __init__(
        self,
        pir_sensor: PIRSensor,
        ultrasonic_sensor: UltrasonicSensor,
    ):
        self.pir_sensor = pir_sensor
        self.ultrasonic_sensor = ultrasonic_sensor

    def _read_sensors_data(self) -> bool | None:
        pir_detection = self.pir_sensor.read_presence()
        distance = self.ultrasonic_sensor.read_distance()

        # Brak danych z obu czujników
        if pir_detection is None and distance is None:
            return None

        # Ocena odległości: obiekt w pobliżu
        nearby_object = (
            distance is not None
            and 2 <= distance <= 200
        )

        # PIR wykrył ruch lub ultradźwięki wykryły bliski obiekt
        if pir_detection is True or nearby_object:
            return True

        # Oba czujniki działają i nie wskazują na obecność
        if pir_detection is False and distance is not None:
            return False

        # Jeden czujnik nie działa, a drugi nie wskazuje obecności
        return None

    def detect_presence(self) -> bool | None:
        return self._read_sensors_data()
