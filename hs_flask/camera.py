import time
import io
import threading
import picamera

class Camera(object):
    thread = None
    frame = None
    last_access = 0
    thread_controller = True

    def initialize(self):
        if Camera.thread is None:
            self.thread_controller = True
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()
            while self.frame is None:
                time.sleep(0)

    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame

    def thread_stop(self):
        Camera.thread_controller = False
   
    def return_thread_controller(self):
        return Camera.thread_controller
 
    @classmethod
    def _thread(cls):
        with picamera.PiCamera() as camera:
            print 'start of thread'
            camera.resolution = (480, 360)
            camera.hflip = True
            camera.vflip = True

            camera.start_preview()
            time.sleep(2)

            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                if cls.thread_controller == False:
                    print 'quit thread'
                    cls.thread = None
                    break
                stream.seek(0)
                cls.frame = stream.read()

                stream.seek(0)
                stream.truncate()
                if time.time() - cls.last_access > 10:
                    break
        cls.thread = None
        cls.thread_controller = True
        print 'End of Thread'
