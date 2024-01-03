import RPi.GPIO as GPIO
from time import sleep
SERVO_PIN = 17                                                           # Servo pin
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)                   # Setup for the Servo, GPIO,

# --Servo Code-- #

def setAngle(srv, angle):                                            #General method to move the servo to the specified angle
    dc = (angle/180 * 10) +2.5                                     # Calculates the duty cycle
    srv.ChangeDutyCycle(dc)                                       # Sends the PWM Signal
    sleep(1)

servo = GPIO.PWM(SERVO_PIN, 50)                    #Sets the PWM to 50Hz

servo.start(2.5)                                                              # Start at position 0

for angle in range (0, 175, 5):
    setAngle(servo, angle)                                            # Moves the servo to 180 in steps of 5
    
# --Servo Code-- #

#PWM.stop()
GPIO.cleanup()