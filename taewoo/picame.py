from time import sleep
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (160, 120)
camera.rotation = 180
camera.start_preview()
# Camera warm-up time
sleep(2)
i=0
while True:
    camera.capture('images/image%s.jpg' %i)
    i+=1
    sleep(0.5) 
