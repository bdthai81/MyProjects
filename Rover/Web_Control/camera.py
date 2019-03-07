import picamera
import time

def capture_image(image_path):
	
	with picamera.PiCamera() as camera:
		camera.resolution = (300, 300)
		camera.capture(image_path)
		camera.close()
