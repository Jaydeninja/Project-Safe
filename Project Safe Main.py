# --                                                                                                                                                                    |-PROJECT SAFE -|                                               Jayden Ellul | Savio College Malta | Last edited: 00:50 2/1/24   - #
## Import libraries
import RPi.GPIO as GPIO                    # GPIO Pins
import cv2                                                 # OpenCV
from picamera import PiCamera       # RPi Camera
import matplotlib.pyplot as plt          # Face Recognition
from time import sleep                         # Delay



# Set up GPIO & Servo
SERVO_PIN = 17
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)



## Takes Picture from the Pi Camera
# Declare camera
camera = PiCamera()

# Adjust window + camera settings
camera.resolution = (320,240)
camera.preview_fullscreen = False
camera.preview_window = (100, 100, 320, 240)
camera.brightness = 60

# Start preview
camera.start_preview()

# Give user time to show his face 
sleep(5)

# Capture face and save it (saves image in the same folder the code is in)
camera.capture('face.jpg')

# Close preview
camera.stop_preview()
sleep(3)


## Detects face from taken picture
# Load the image (looks for the image the same folder the code is in)
image_path = 'face.jpg'
image = cv2.imread(image_path)

# Convert the image to grayscale (required for face detection)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Load the Haar Cascade Classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Detect faces in the grayscale image (Fourhead needs to show and glasses are accepted)
faces = face_cascade.detectMultiScale(gray_image, 1.3, 5)

# Draw rectangles around the detected faces
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

# Display the image with detected face or faces
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()


## Unlocks/locks Safe with servo
# Move servo to specified angle, calculates duty cycle and sets PWM
def setAngle(srv, angle):
    dc = (angle/180 * 10) +2.5
    srv.ChangeDutyCycle(dc)
    sleep(1)

#Sets the PWM to 50Hz
servo = GPIO.PWM(SERVO_PIN, 50)

# Start at position 0
servo.start(2.5)

# Moves the servo to 175(so it doesnt exceed limit) in steps of 7 (for testing, REMOVE LATER)
for angle in range (0, 175, 7):
    setAngle(servo, angle)                                            

## Stop libs
GPIO.cleanup()