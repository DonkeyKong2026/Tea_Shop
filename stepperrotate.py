import time
import RPi.GPIO as GPIO

# DRV8833 input pins (BCM numbers).
# Example wiring: change to match yours.
AIN1 = 23
AIN2 = 27
BIN1 = 22
BIN2 = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(AIN1, GPIO.OUT, initial=0)
GPIO.setup(AIN2, GPIO.OUT, initial=0)
GPIO.setup(BIN1, GPIO.OUT, initial=0)
GPIO.setup(BIN2, GPIO.OUT, initial=0)

# Send one row of the table to the driver.
def set_coils(a1, a2, b1, b2):
    GPIO.output(AIN1, a1)
    GPIO.output(AIN2, a2)
    GPIO.output(BIN1, b1)
    GPIO.output(BIN2, b2)

# Settings
steps_per_rev = 200 # 1.8° full steps
turns = 0.5            # turns to make
rpm = 30             # target speed
direction = 1        # 1 forward, -1 back

# Delay per step in seconds, Eq. (5)
delay = 60 / (steps_per_rev * rpm)
total_steps = int(turns * steps_per_rev)

# Align first; this initial movement is not a counted step.
state = 0
try:
    set_coils(1, 0, 1, 0)
    time.sleep(0.2)  # allow alignment at this starting state
    start = time.perf_counter()
    for step in range(total_steps):
        state = (state + direction) % 4
        if state == 0:
            set_coils(1, 0, 1, 0)  # A+ B+
        elif state == 1:
            set_coils(0, 1, 1, 0)  # A- B+
        elif state == 2:
            set_coils(0, 1, 0, 1)  # A- B-
        else:
            set_coils(1, 0, 0, 1)  # A+ B-
        time.sleep(delay)

    elapsed = time.perf_counter() - start
    print(f"Time: {elapsed:.2f} s")
    print(f"Average RPM: {turns * 60 / elapsed:.1f}")
finally:
    set_coils(0, 0, 0, 0)  # release coils even after Ctrl-C
    GPIO.cleanup()