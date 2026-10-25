from services.sensors.environment import EnvironmentSensor


def test_read_all_returns_all_measurements():
    sensor = EnvironmentSensor(
        failure_probability=0,
        disturbance_probability=0,
    )

    readings = sensor.read_all()

    assert set(readings.keys()) == {
        "temperature",
        "humidity",
        "light",
        "sound",
    }


def test_sensor_can_return_none():
    sensor = EnvironmentSensor(
        failure_probability=1,
        disturbance_probability=0,
    )

    readings = sensor.read_all()

    assert all(value is None for value in readings.values())


def test_normal_measurements_are_within_ranges():
    sensor = EnvironmentSensor(
        failure_probability=0,
        disturbance_probability=0,
    )

    readings = sensor.read_all()

    assert -10 <= readings["temperature"] <= 35
    assert 20 <= readings["humidity"] <= 80
    assert 0 <= readings["light"] <= 100
    assert 0 <= readings["sound"] <= 100