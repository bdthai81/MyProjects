import maestro
import time

# Set channels: v=veritcal, h=horizontal
v_channel = 0
h_channel = 1

# first element and last element are the minimum and maxium positions for the servos
# in quarter-microseconds. The defaults are set on the board. See the Maestro
# manual for how to change these values. The factory defaults are 992us and
# 2000us.
# Allowing quarter-microseconds gives you more resolution to work with.
# e.g. If you want a maximum of 2000us then use 8000us (4 x 2000us).

# Kept range in Pololu maestro control center at 608-2544 [down, center, up]
v_pos = [1300*4, 1700*4, 2100*4]
# Changed range in Pololu maestro control center to 608-2544 [right, center, left]
h_pos = [650*4, 1500*4, 2480*4]


def	center():
	"""Center camera view"""
	# Open controller session
	servo = maestro.Controller()
	servo.setTarget(v_channel, v_pos[1])
	servo.setTarget(h_channel, h_pos[1])
		
	# Close controller session
	servo.close()

def	T_D_():
	"""Tilt down on camera view"""
	# Open controller session
	servo = maestro.Controller()
	# Check position to see if we're out of bound to tilt down
	v_ix = v_pos.index(servo.getPosition(v_channel))
	if v_ix < (len(v_pos)-1):
		# not out of bound to tilt 1 more position
		servo.setTarget(v_channel, v_pos[v_ix+1])
		
	# Close controller session
	servo.close()
	
def	T_U_():
	"""Tilt up on camera view"""
	# Open controller session
	servo = maestro.Controller()
	# Check position to see if we're out of bound to tilting up
	v_ix = v_pos.index(servo.getPosition(v_channel))
	if v_ix > 0:
		# not out of bound to tilt 1 more position
		servo.setTarget(v_channel, v_pos[v_ix-1])
		
	# Close controller session
	servo.close()
	
def T_L_():
	"""Tilt left on camera view"""
	# Open controller session
	servo = maestro.Controller()
	# Check position to see if we're out of bound to tilt down
	h_ix = h_pos.index(servo.getPosition(h_channel))
	if h_ix < (len(h_pos)-1):
		# not out of bound to tilt 1 more position
		servo.setTarget(h_channel, h_pos[h_ix+1])
				
	# Close controller session
	servo.close()

def	T_R_():
	"""Tilt right on camera view"""
	# Open controller session
	servo = maestro.Controller()
	# Check position to see if we're out of bound to tilting up
	h_ix = h_pos.index(servo.getPosition(h_channel))
	if h_ix > 0:
		# not out of bound to tilt 1 more position
		servo.setTarget(h_channel, h_pos[h_ix-1])
			
	# Close controller session
	servo.close()
	
