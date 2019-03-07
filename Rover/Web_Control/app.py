from flask import Flask, render_template, redirect, request, jsonify
import json
import motor
import camera
import base64

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/command", methods=["POST"])
def command():
    # Load variable
    content = request.get_json()
    webCommand = content["webCommand"]
    
    print(webCommand)
    # Execute action of request movement
    results = getattr(motor, webCommand)()
   
    return jsonify(webCommand=webCommand)

@app.route("/stop_motion", methods=["POST"])
def stop_motion():
    motor.stop_motion()
    
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

if __name__ == "__main__":
    app.run(host='192.168.0.112', debug=True)
