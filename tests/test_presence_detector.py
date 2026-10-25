import pytest
from unittest.mock import Mock

from services.sensors.detector import PresenceDetector


@pytest.fixture
def sensors():
    pir_sensor = Mock()
    ultrasonic_sensor = Mock()

    detector = PresenceDetector(pir_sensor, ultrasonic_sensor)

    return detector, pir_sensor, ultrasonic_sensor


def test_presence_detected_by_pir(sensors):
    detector, pir_sensor, ultrasonic_sensor = sensors

    pir_sensor.read_presence.return_value = True
    ultrasonic_sensor.read_distance.return_value = 300

    assert detector.detect_presence() is True


def test_no_presence_detected(sensors):
    detector, pir_sensor, ultrasonic_sensor = sensors

    pir_sensor.read_presence.return_value = False
    ultrasonic_sensor.read_distance.return_value = 300

    assert detector.detect_presence() is False


def test_presence_detected_when_pir_fails(sensors):
    detector, pir_sensor, ultrasonic_sensor = sensors

    pir_sensor.read_presence.return_value = None
    ultrasonic_sensor.read_distance.return_value = 100

    assert detector.detect_presence() is True


def test_unknown_when_both_sensors_fail(sensors):
    detector, pir_sensor, ultrasonic_sensor = sensors

    pir_sensor.read_presence.return_value = None
    ultrasonic_sensor.read_distance.return_value = None

    assert detector.detect_presence() is None


def test_no_presence_when_pir_reports_false_and_object_is_far(sensors):
    detector, pir_sensor, ultrasonic_sensor = sensors

    pir_sensor.read_presence.return_value = False
    ultrasonic_sensor.read_distance.return_value = 350

    assert detector.detect_presence() is False


def test_presence_detected_at_distance_boundary(sensors):
    detector, pir_sensor, ultrasonic_sensor = sensors

    pir_sensor.read_presence.return_value = False
    ultrasonic_sensor.read_distance.return_value = 200

    assert detector.detect_presence() is True