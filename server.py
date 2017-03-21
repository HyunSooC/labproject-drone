#/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep

PORT_NUMBER = 8088
import urlparse
import spidev
import argparse
import sys
import threading
from picamera import PiCamera
from time import sleep

def th_TakePicture():
	i=0
	picam = PiCamera()
	picam.rotation = 180;
	while i<50:
		i+=1
		sleep(2)
		print 'take picture', i
		picam.capture('current_img.jpg')
	picam.close()
	print 'finish thread'	

class myHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		parsed_path = urlparse.urlparse(self.path)
		parsed_path
		print "request:",parsed_path.path
		print "querry:", parsed_path.query
		print "self.path:", self.path
		if self.path.endswith("bt2"):
			print "take picture hello.jpg"
			jpgth = threading.Thread(target=th_TakePicture, args=())
			jpgth.start()
		if self.path=="/":
			self.path="dronecontroller.html"
		
		try:
			sendReply = False
			if parsed_path.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True                    
			if self.path.endswith(".jpg"):
				print "requested jpg"
                                mimetype='image/jpg'
                                sendReply = True

			if sendReply == True:
				#Open the static file requested and send it
				f = open(curdir + sep + parsed_path.path) 
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
			return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

server = HTTPServer(('', PORT_NUMBER), myHandler)
print 'Started httpserver on port ' , PORT_NUMBER
server.serve_forever()
server.socket.close()
