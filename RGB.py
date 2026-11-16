import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)


class RGB:
    def __init__(self, red, green, blue, Freq=100):
        
        self.pwm =[]
        for p in (red, green ,blue):
            GPIO.setup(p, GPIO.OUT)
            ch = GPIO.PWM(p, Freq)
            ch.start(0)
            self.pwm.append(ch)
        

    def color(self, r, g, b):
        for ch, v in zip(self.pwm, (r, g, b)):
            ch.ChangeDutyCycle(v / 255 * 100)
    def cycle(self):
        H = 255
        L = 0
        cyc = [(H, L, L), (L, H, L), (L, L, H), (H, H, L), (L, H, H), (H, L, H), (H, H, H)]
        for i in cyc:
            self.color(*i)
            print(i)
            time.sleep(5)
    def off(self, r, g, b):
        self.set_color(0,0,0)
    
    def cleanup(self):
        for ch in self.pwm:
            ch.stop()
            GPIO.cleanup()

