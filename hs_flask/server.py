from flask import Flask, render_template, stream_with_context, Response, request
from camera import Camera
import spidev
import time
import argparse 
import sys
import navio.mpu9250
import navio.util

app = Flask(__name__, static_folder = "img")

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'GET':
    print 'request is get'
  if request.method == 'POST':
    print 'request is post'
  return render_template('drone.html')

@app.route('/drone.html')
def drone():
  print 'server is requested drone.html'
  return render_template('drone.html')

@app.route('/visualization')
def test():
  if request.headers.get('accept') == 'text/event-stream':
    def events():
       navio.util.check_apm()
       imu = navio.mpu9250.MPU9250()
       if imu.testConnection():
         print "Connection established: True"
       else:
         sys.exit("Connection established: False")
       imu.initialize()
       time.sleep(0.5)
       while(True):
         m9a, m9g, m9m = imu.getMotion9()
         yield "data:%s\n\n" % format(m9a)
         time.sleep(.1)
    return Response(events(), content_type='text/event-stream')
  return redirect(url_for('templates', filename='drone.html'))

   #m9a, m9g, m9m = imu.getMotion9()
   #print "Acc:", "{:+7.3f}".format(m9a[0]), "{:+7.3f}".format(m9a[1]), "{:+7.3f}".format(m9a[2]),
   #print " Gyr:", "{:+8.3f}".format(m9g[0]), "{:+8.3f}".format(m9g[1]), "{:+8.3f}".format(m9g[2]),
   #print " Mag:", "{:+7.3f}".format(m9m[0]), "{:+7.3f}".format(m9m[1]), "{:+7.3f}".format(m9m[2])
   #return format(m9a)

#@app.route('/stream')
#def streamed_response():
#   def generate():
#      i = 0
#      while i<2:
#         print 'generate function'
#         yield 'Hello '
#         yield format(i)
#         i+=1
#         time.sleep(5)
#   return Response(stream_with_context(generate()))

def gen(camera):
  while camera.return_thread_controller() == True:
    frame = camera.get_frame()
    yield (b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
  return Response(gen(Camera()),
    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_stop')
def video_stop():
  print 'video_stop function'
  Camera().thread_stop()
  return 'ok'
  #return send_file('/home/pi/hs/flask/no.jpg', attachment_filename='no.jpg')

@app.route('/three.min.js')
def three():
  return render_template('three.min.js') 

if __name__ == '__main__':
  boolmain = True
  app.run(host='192.168.0.30', debug=True, threaded=True)
