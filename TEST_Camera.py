## Import libraries
import cv2                                                 # OpenCV
from picamera import PiCamera       # RPi Camera
import matplotlib.pyplot as plt          # Face Recognition
from time import sleep                         # Delay



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

