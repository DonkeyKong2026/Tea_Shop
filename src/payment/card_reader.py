"""Card tap detection for the payment screen, using an HC-SR04 ultrasonic sensor.

A "card tap" is any object held within TAP_DISTANCE_CM of the sensor for a few
readings in a row.

Wiring (BCM pin numbers):
- VCC to 5V
- GND to any ground pin
- TRIG to GPIO 5
- ECHO to GPIO 6 through a voltage divider: 1 kOhm in series from ECHO to
  GPIO 6, and 2 kOhm from GPIO 6 to ground. ECHO outputs 5V, which would damage
  the Pi's 3.3V GPIO pins without the divider.

Run this file on its own to test the wiring: it prints live distances and
reports each tap.
"""

import time

import RPi.GPIO as GPIO

TRIG_PIN = 5
ECHO_PIN = 6

TAP_DISTANCE_CM = 10
REQUIRED_CONSECUTIVE_HITS = 3

SPEED_OF_SOUND_CM_PER_S = 34300
TRIGGER_PULSE_S = 10e-6
ECHO_TIMEOUT_S = 0.03
SETTLE_TIME_S = 0.05


class HCSR04:
    """Driver for one HC-SR04 ultrasonic distance sensor."""

    def __init__(self, trig_pin: int = TRIG_PIN, echo_pin: int = ECHO_PIN):
        """Set up the trigger pin as an output held low and the echo pin as an input."""
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.echo_pin, GPIO.IN)
        time.sleep(SETTLE_TIME_S)

    def read_distance_cm(self) -> float | None:
        """Measure the distance to the nearest object, in centimeters.

        Returns None if no echo arrives within ECHO_TIMEOUT_S, so a missing
        sensor or out-of-range reading never blocks the caller for long.
        """
        GPIO.output(self.trig_pin, GPIO.HIGH)
        time.sleep(TRIGGER_PULSE_S)
        GPIO.output(self.trig_pin, GPIO.LOW)

        echo_rise_s = self._wait_for_echo_level(GPIO.HIGH)
        if echo_rise_s is None:
            return None
        echo_fall_s = self._wait_for_echo_level(GPIO.LOW)
        if echo_fall_s is None:
            return None

        round_trip_s = echo_fall_s - echo_rise_s
        return round_trip_s * SPEED_OF_SOUND_CM_PER_S / 2

    def cleanup(self):
        """Release the trigger and echo pins."""
        GPIO.cleanup((self.trig_pin, self.echo_pin))

    def _wait_for_echo_level(self, level: int) -> float | None:
        """Wait for the echo pin to reach the given level.

        Returns the time it got there, from time.perf_counter(), or None on timeout.
        """
        deadline_s = time.perf_counter() + ECHO_TIMEOUT_S
        while GPIO.input(self.echo_pin) != level:
            if time.perf_counter() > deadline_s:
                return None
        return time.perf_counter()


class CardReader:
    """Turns raw distance readings into card taps for the payment screen."""

    def __init__(
        self,
        sensor: HCSR04,
        tap_distance_cm: float = TAP_DISTANCE_CM,
        required_hits: int = REQUIRED_CONSECUTIVE_HITS,
    ):
        """Wrap a sensor; a tap needs required_hits readings in a row under tap_distance_cm."""
        self.sensor = sensor
        self.tap_distance_cm = tap_distance_cm
        self.required_hits = required_hits
        self.consecutive_hits = 0
        self.last_distance_cm = None

    def check_for_tap(self) -> bool:
        """Take one reading and return True once enough close readings arrive in a row.

        This does not block, so a UI can call it on a timer. The count resets
        after a tap so the same card is not counted twice.
        """
        distance_cm = self.sensor.read_distance_cm()
        self.last_distance_cm = distance_cm
        is_close = distance_cm is not None and distance_cm < self.tap_distance_cm
        self.consecutive_hits = self.consecutive_hits + 1 if is_close else 0

        if self.consecutive_hits >= self.required_hits:
            self.reset()
            return True
        return False

    def reset(self):
        """Forget any partial tap, for example when a new payment starts."""
        self.consecutive_hits = 0


def run_wiring_test():
    """Print live distances and report taps until stopped with Ctrl-C."""
    sensor = HCSR04()
    card_reader = CardReader(sensor)
    try:
        while True:
            is_tapped = card_reader.check_for_tap()
            distance_cm = card_reader.last_distance_cm
            if distance_cm is None:
                print("No echo")
            else:
                print(f"Distance: {distance_cm:.1f} cm")
            if is_tapped:
                print("Card tapped")
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        sensor.cleanup()


if __name__ == "__main__":
    run_wiring_test()
