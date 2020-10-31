from flask import Flask, render_template, Response 
import picamera
import sys

ROTATION = sys.argv[1] if len(sys.argv) > 1 else 0
print('video captured is rotated by : ' +  str(ROTATION) + ' degrees')

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/welcome')
def welcome():
	return 'Hello world'


def collect_images():
	#initialize picamera module once to avoid memory errors (too many apps uusing camera)
	with picamera.PiCamera() as camera:
		while(1):
			camera.start_preview()
			camera.capture('image.jpg')
			camera.stop_preview()
			yield (b'--frame\r\n' 
                b'Content-Type: image/jpeg\r\n\r\n' + open('image.jpg', 'rb').read() + b'\r\n') 




@app.route('/video_feed')
def video_feed():
	return Response(collect_images(),mimetype='multipart/x-mixed-replace; boundary=frame')	


if __name__ == '__main__':
	
	app.run(host='0.0.0.0', debug=True,threaded=True)
