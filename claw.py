import time
import RPi.GPIO as GPIO

SERVO = 18
ZERO_DUTY = 7.5
DEG_PER_CYCLE  = 24.0

ANGLE = 120

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO, GPIO.OUT)
pwm = GPIO.PWM(SERVO, 50)

try:
    pwm.start(ZERO_DUTY)
    time.sleep(1)

    duty = ZERO_DUTY + ANGLE/ DEG_PER_CYCLE
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)

    pwm.ChangeDutyCycle(ZERO_DUTY)
    time.sleep(1)

finally:
    pwm.stop()
    GPIO.cleanup()
