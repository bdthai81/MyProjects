Objective: Utilize reinforcement learning, so rover can auto-pilot.

Phase 1:
* Assembled rover (File "Rover Parts List", contains the core parts used)
* Wired motors with H Bridge & Raspberry Pi 3b+
* Setup Raspberry Pi 3B+ env. w/ anaconda (File "Rover Env Setup", describe the steps taken)
* Coded Motor.py to test rover motions: forward, reverse, turn left, turn right, pivot left, and pivot right
* uploaded image of rover

Phase 2:
* Coded Web Control webpage: bootstrap, svg, javascript
  - Made web control buttons from svg. 
* Integrated Flask with web control and motor.py: Python, Ajax, D3
  - Mouse/Touch screen: on click, motor will run for 0.1s. on hold, motor will run increments of 0.5s continuously.
