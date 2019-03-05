from flask import Flask, render_template, redirect, request, jsonify
import json
import motor

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/command", methods=["POST"])
def command():
    # Load variables
    content = request.get_json()
    webCommand = content["webCommand"]
    tf = content["tf"]
    
    # Execute action of request movement
    results = getattr(motor, webCommand)(tf)
   
    #return '{"data":"test"}'
    return jsonify(webCommand=webCommand, tf=results)


if __name__ == "__main__":
    app.run(debug=True)