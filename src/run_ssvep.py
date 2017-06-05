#!/usr/bin/env python
#author:John Naulty
#date: july 2014
#SSVEP Example with Psychopy and OpenBCI
#stimuli frequency = 60/(frame_on+frame_off)

from time import sleep
from SSVEP import *
# from InputBox import InputBox
# import csv_collector
import rospy
from openbci.msg import BCIuVolts
#expinfos = InputBox()
filename = ''#expinfos.file()
port_addr = ''#expinfos.port_name()
flash_dur = 10000#expinfos.stim_duration()
trialnums = 1#expinfos.stim_trials()
waitduration = 0#expinfos.waitduration()
# frequency = expinfos.frequency()

def ssvep_one():

	rospy.init_node('ssvep_10', anonymous=True)
	pub = rospy.Publisher('chatter_10', BCIuVolts, queue_size=1)
	while not rospy.is_shutdown():
		stimuli6=SSVEP(frame_on=3, frame_off=3, fname=filename, port=port_addr,
			trialdur=flash_dur, numtrials=trialnums, waitdur=waitduration, mywin = (0,200))
		stimuli6.start()



#set of stimuli followed by frequency of stimuli. 

"""
stimuli75 = SSVEP(frame_on=4, frame_off=4, fname=filename, port=port_addr, trialdur=flash_dur, numtrials=trialnums, waitdur=waitduration)
stimuli75.start()
print 1
"""
"""
stimuli12=SSVEP(frame_on=3, frame_off=2, fname=filename, port=port_addr,
	trialdur=flash_dur, numtrials=trialnums, waitdur=waitduration)
stimuli12.start()
print 2
"""
'''
pairs = [(3,3)]
n_trials = 1000
msg = BCIuVolts()
msg.data = [0]
for trial in range(0,n_trials):
	print trial
	for pair in pairs:
		if pair[0] == 3 and pair[1] == 3:
			msg.data[0] = 4
		#elif pair[0] == 3:
			#msg.data[0] = 2
		#elif pair[0] == 2:
			#msg.data[0] = 3

		#sleep(5)
		stimuli6=SSVEP(frame_on=pair[0], frame_off=pair[1], fname=filename, port=port_addr,
			trialdur=flash_dur, numtrials=trialnums, waitdur=waitduration)
		#stamp = rospy.get_rostime()
		#msg.stamp = stamp
		#pub.publish(msg)
		stimuli6.start()
		#stamp = rospy.get_rostime()
		#msg.stamp = stamp
		#pub.publish(msg)
		

	# stimuli10=SSVEP(frame_on=3, frame_off=3, fname=filename, port=port_addr,
	# 	trialdur=flash_dur, numtrials=trialnums, waitdur=waitduration)
	# stimuli10.start()


	# stimuli15=SSVEP(frame_on=2, frame_off=2, fname=filename, port=port_addr,
	# 	trialdur=flash_dur, numtrials=trialnums, waitdur=waitduration)
	# stimuli15.start()

'''
if __name__ == '__main__':
    try:
        ssvep_one()
    except rospy.ROSInterruptException:
        pass