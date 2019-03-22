from flask import Flask, render_template, redirect, request, jsonify
import RPi.GPIO as GPIO
import json
import motor
import camera
import camera_tilt
import sensor
import base64

app = Flask(__name__)

# Define function name list to match WebControl
motor_commands = ["Forward", "Reverse", "Left", "Right", "Pivot_Left", "Pivot_Right"]
camera_tilt_commands = ["T_D_", "T_U_", "T_L_", "T_R_"]

# Setup GPIO mode to Boardcom SOC channel
GPIO.setmode(GPIO.BCM)

# Create motor object
mo = motor.Motor()
# Create camera tilt object
cto = camera_tilt.Camera_tilt()
# Create Sensor object
so = sensor.Sensor()

#GPIO.cleanup()
# Close controller session
#servo.close()

@app.route("/")
def index():
    # Center camera view, use as default
    cto.center()
    
    return render_template("index.html")

@app.route("/command", methods=["POST"])
def command():
    # Load variable
    content = request.get_json()
    web_command = content["webCommand"]
    
    # Determine if webCommand is a motor or tilt_camera command, then execute command
    if web_command in motor_commands:
        # Execute action of request movement
        results = getattr(mo, web_command)()
    elif web_command in camera_tilt_commands:
        # Execute action of request movement
        results = getattr(cto, web_command)()
   
    return jsonify(webCommand=web_command)

@app.route("/stop_motion", methods=["POST"])
def stop_motion():
    mo.stop_motion()
    
    return ""

@app.route("/center_camera", methods=["POST"])
def center_camera():
    # Center camera view, use as default
    cto.center()
    
    return ""

@app.route("/camera_image", methods=["POST"])
def camera_image():
    # Load variables
    content = request.get_json()
    imgName = content["imgName"]
    # capture image
    camera.capture_image(imgName)
    # convert image into base64
    #with open("./camera_imgs/rover_view.png", "rb") as image_file:
    #    encoded_string = base64.b64encode(image_file.read())
    
    return ""
    
@app.route("/sensors_distance", methods=["POST"])
def sensors_distance():
    # Run sensors
    results = so.runSensors()
    
    return ", ".join([str(i) for i in results])

if __name__ == "__main__":
    app.run(host='192.168.0.112', debug=True)
