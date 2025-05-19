import RPi.GPIO as GPIO                                   # GPIO Pins
import cv2                                                                # Camera
import time                                                              # Datetime of file
from pydub import AudioSegment                  # Audio controler
from pydub.playback import play                    # Play sounds
from picamera2 import Picamera2,Preview # Preview
from picamera2.previews import QtGlPreview
from libcamera import Transform                   # Recording
from time import sleep                                        # Delay

#Configuration of application
debug =  False
picamFormat = "RGB888"
filename = "snapshots/"+time.strftime("%Y%m%d-%H%M%S") + ".jpg"
tries = 3
attempts = 0
correctpass = "0000"
lockbackkey = "*"

# Config - Set up GPIO & Servo
SERVO_PIN = 17
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
servo = GPIO.PWM(SERVO_PIN, 50)

# Config - Set up paths for sounds
shutdown = AudioSegment.from_file("/home/robotics/Desktop/Folders/Codes/Project Safe/Wav/shutdown.wav")
startup = AudioSegment.from_file("/home/robotics/Desktop/Folders/Codes/Project Safe/Wav/startup.wav")
error = AudioSegment.from_file("/home/robotics/Desktop/Folders/Codes/Project Safe/Wav/error.wav")
alarm = AudioSegment.from_file("/home/robotics/Desktop/Folders/Codes/Project Safe/Wav/alarm.wav")
check = AudioSegment.from_file("/home/robotics/Desktop/Folders/Codes/Project Safe/Wav/check.wav")

#Method to capture and detect face
def DFace():
    print("Please stand in front of camera to start.")
    
    # Load the pre-trained Haar Cascade classifier for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    picam2 = Picamera2()
    picam2. start_preview(Preview. QT)
    picam2.start()
    

    try:
        while True:
            im = picam2.capture_array()
    
            # Convert the image to grayscale for face detection
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

            # Perform face detection
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

            if debug == True:
                # Draw rectangles around the detected faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(im, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
            if len(faces) > 0 :
                # Save img to file
                cv2.imwrite(filename,im)
            
                break
        
        #at this point it means that a face has been detected
        print ("Face detected ...")

       #check passcode
        PassCodeEntry();

    finally:
        # Release resources
        cv2.destroyAllWindows()
        picam2.stop()
        picam2.close()

#Method to accept passcode from keypad
def PassCodeEntry():
    print("Passcode entry")
    safeopened = False

    for attempts in range(tries):
        if (safeopened == False):
              passcode = input("Enter Pin via Keypad. (" + str(attempts+1) + "/" + str(tries) +")")
              
              if (passcode == correctpass):
                  OpenSafe();
                  play(check)
                  safeopened = True;
              else:
                  print("Incorrect passcode")
                  if (attempts == 2) : print("Too many incorrect tries. Program will exit.")
                  play(alarm)


# Move servo to specified angle, calculates duty cycle and sets PWM
def setAngle(srv, angle):
    dc = (angle/180 * 10) +2.5
    srv.ChangeDutyCycle(dc)
    sleep(1)

#Method to close safe lock - Locks Safe with servo
def CloseSafe():
    servo.start(2.5)
    setAngle(servo, 90)

#Method to open safe lock - Unlocks Safe with servo
def OpenSafe():
    servo.start(2.5)
    setAngle(servo, 0)
    
    print("Safe opened.")
    play(check)
    
    looplock = True
    while looplock:        
            keypress = input("PRESS " + lockbackkey + " TO LOCK AGAIN")
            if keypress == lockbackkey:
                CloseSafe();
                play(check)
                looplock = False;

    GPIO.cleanup()  

#-----Start program-----

play(startup)
CloseSafe() #reset safe to closed position

DFace();

print("Thanks for using SAFE SYSTEMS.")
play(shutdown)
