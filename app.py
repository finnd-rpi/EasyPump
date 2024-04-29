# EasyPump is created by Claudio Lo Preiato for personal purpose, to control a PEDROLLO SUBMERSIBLE PUMP

from flask import Flask, request, render_template, redirect, url_for, send_file
import atexit
import time
import RPi.GPIO as GPIO

# Define Variables
relay_pin = 17
button_state = "OFF"

# GPIO Pins setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)

# Defining GPIO's control functions
def turn_on_relay(pin):
    GPIO.output(pin, GPIO.HIGH)

def turn_off_relay(pin):
    GPIO.output(pin, GPIO.LOW)

def cleanup_gpio():
    global button_state
    button_state = "OFF"
    turn_off_relay(relay_pin)
    GPIO.cleanup()

# Istantiate a new Flask app
app = Flask(__name__)

# Main page route
@app.route('/', methods=["GET"])
def index():
    return render_template('index.html', button_state=button_state)

# Processing income data to control GPIO pins
@app.route('/pump_status', methods=['POST'])
def update_pump_status():
    global button_state
    button_state = request.form['status']
    if button_state == 'ON':
        turn_on_relay(relay_pin)
    elif button_state == 'OFF':
        turn_off_relay(relay_pin)
    return redirect(url_for("index"))

# Serving manifest.json file to use the web page as PWA (Progressive Web App)
@app.route('/manifest.json')
def serve_manifest():
    return send_file('manifest.json', mimetype='application/manifest+json')

# Runs 'cleanup_up' function if the flask server closes
atexit.register(cleanup_gpio)

# Uncomment the lines below if you are not using a WSGI server like gunicorn
#if __name__ == '__main__':
#	app.run(debug=True, host='0.0.0.0', port=5000)
