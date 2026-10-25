from services.sensors.presence import PIRSensor


def test_read_return():
    sensor = PIRSensor(
        failure_probability=0,
        disturbance_probability=0,
    )

    readings = sensor.read_presence()

    assert readings is not None


def test_sensor_can_return_none():
    sensor = PIRSensor(
        failure_probability=1,
        disturbance_probability=0,
    )

    readings = sensor.read_presence()

    assert readings is None

def test_sensor_can_return_true():
    sensor = PIRSensor(
        failure_probability=0,
        disturbance_probability=1,
    )

    readings = sensor.read_presence()

    assert readings is True

from services.sensors.presence import UltrasonicSensor


def test_read_distance_return():
    sensor = UltrasonicSensor(
        failure_probability=0,
        disturbance_probability=0,
    )

    readings = sensor.read_distance()

    assert readings is not None


def test_sensor_can_return_none():
    sensor = UltrasonicSensor(
        failure_probability=1,
        disturbance_probability=0,
    )

    readings = sensor.read_distance()

    assert readings is None


def test_normal_measurements_are_within_ranges():
    sensor = UltrasonicSensor(
        failure_probability=0,
        disturbance_probability=0,
    )

    readings = sensor.read_distance()

    assert 2 <= readings <= 400