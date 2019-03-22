import maestro
from settings import H_SERVO, V_SERVO, H_POS, V_POS
import time

class Camera_tilt:
	
	def __init__(self):
		"""
		Declare maestro controller object
		"""
		self.servo = maestro.Controller()
		
	def	center(self):
		"""
		Default camera position to center
		"""
		try:
			self.servo.setTarget(V_SERVO, V_POS[1])
			self.servo.setTarget(H_SERVO, H_POS[1])
		except:
			# User might request faster than camera can tilt
			pass
		
	def	T_D_(self):
		"""Tilt down on camera position"""
		try:
			# Check position to see if we're out of bound to tilt down
			v_ix = V_POS.index(self.servo.getPosition(V_SERVO))
			if v_ix < (len(V_POS)-1):
				# not out of bound, tilt one position down
				self.servo.setTarget(V_SERVO, V_POS[v_ix+1])
		except:
			# User might request faster than camera can tilt
			pass
			
	def	T_U_(self):
		"""Tilt up on camera position"""
		try:
			# Check position to see if we're out of bound to tilt up
			v_ix = V_POS.index(self.servo.getPosition(V_SERVO))
			if v_ix > 0:
				# not out of bound to tilt 1 more position
				self.servo.setTarget(V_SERVO, V_POS[v_ix-1])
		except:
			# User might request faster than camera can tilt
			pass
			
	def T_L_(self):
		"""Tilt left on camera position"""
		try:
			# Check position to see if we're out of bound to tilt left
			h_ix = H_POS.index(self.servo.getPosition(H_SERVO))
			if h_ix < (len(H_POS)-1):
				# not out of bound to tilt 1 more position
				self.servo.setTarget(H_SERVO, H_POS[h_ix+1])
		except:
			# User might request faster than camera can tilt
			pass
		
	def	T_R_(self):
		"""Tilt right on camera position"""
		try:
			# Check position to see if we're out of bound to tilt right
			h_ix = H_POS.index(self.servo.getPosition(H_SERVO))
			if h_ix > 0:
				# not out of bound to tilt 1 more position
				self.servo.setTarget(H_SERVO, H_POS[h_ix-1])
		except:
			# User might request faster than camera can tilt
			pass
				
