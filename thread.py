import threading
from picamera import PiCamera
from time import sleep

def take_thread():
    i=0
    while i<5:
        print "take a picture"
	i+=1
        sleep(0.3)

#camera = PiCamera()
#camera.resolution  = (1024, 768)
#camera.start_preview()
sleep(1)
#camera.capture('asdf.jpg')

th = threading.Thread(target=take_thread, args=())
th.start()
th.join()
print 'finish main'
