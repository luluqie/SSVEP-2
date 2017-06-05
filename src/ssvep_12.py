#!/usr/bin/env python
from time import sleep
from SSVEP import *
import rospy
from openbci.msg import BCIuVolts
filename = ''#expinfos.file()
port_addr = ''#expinfos.port_name()
flash_dur = 10000#expinfos.stim_duration()
trialnums = 1#expinfos.stim_trials()
waitduration = 0#expinfos.waitduration()

def ssvep_one():

	rospy.init_node('ssvep_12', anonymous=True)
	pub = rospy.Publisher('chatter_12', BCIuVolts, queue_size=1)
	while not rospy.is_shutdown():
		stimuli6=SSVEP(frame_on=3, frame_off=2, fname=filename, port=port_addr,
			trialdur=flash_dur, numtrials=trialnums, waitdur=waitduration, mask = 'circle',mywin=(900,200))
		stimuli6.start()

if __name__ == '__main__':
    try:
        ssvep_one()
    except rospy.ROSInterruptException:
        pass		
