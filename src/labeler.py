#!/usr/bin/env python
import struct
import math
import rospy
import numpy as np
import matplotlib.pyplot as plt
from numpy import genfromtxt
from time import sleep
from scipy.signal import lfilter, get_window, butter
import pandas

def cleanize(channel):

	idx = len(channel)-1
	idx2 = len(channel)
	lag = channel[0:idx]
	reg = channel[1:idx2]
	cleaned_sig = (1/math.sqrt(2))*(reg-lag)
	return cleaned_sig

def set_interval(filename):
	run_data = pandas.read_csv(filename, sep=', ')
	run_data_matrix = pandas.DataFrame.as_matrix(run_data)
	begin = []
	end = []
	label = []
	for x in range(0,len(run_data_matrix)):
		if x%2 == 0:
			begin.append(run_data_matrix[x][0])
			label.append(run_data_matrix[x][1])
			end.append(run_data_matrix[x+1][0])
			label.append(run_data_matrix[x+1][1])
			assert((label[x] - label[x+1]) == 0)

	return (begin,end,label)		

def set_label_and_clean(label_file, data_file, new_file):
	begin, end, label = set_interval(label_file)
	channel_data = pandas.read_csv(data_file, sep=',')
	channel_data_matrix = pandas.DataFrame.as_matrix(channel_data)
	jprime = 0
	for i in range(0,len(begin)):
		for j in range(jprime, len(channel_data_matrix)):
			data_time_val = channel_data_matrix[j][0]
			start_time = begin[i]
			stop_time = end[i]
			if data_time_val>=start_time and data_time_val<=stop_time:
				new_label_value = label[i*2]
				#only the column index of the statement below needs to be changed when reducing or expanding the number of channels (represents which column label value is in)
				channel_data_matrix[j][2] = new_label_value
			elif data_time_val>stop_time:
				jprime = j
				break 
			else:
				continue 

	channel1 = channel_data_matrix[:,1]
	channel2 = channel_data_matrix[:,2]
	#channel3 = channel_data_matrix[:,3]			
	#channel4 = channel_data_matrix[:,4]
	#channel5 = channel_data_matrix[:,5]
	#channel6 = channel_data_matrix[:,6]
	#channel7 = channel_data_matrix[:,7]
	#channel8 = channel_data_matrix[:,8]

	#channel_data_matrix[0:len(cleanize(channel1)),1] = cleanize(channel1)
	#channel_data_matrix[0:len(cleanize(channel2)),2] = cleanize(channel2)
	#channel_data_matrix[0:len(cleanize(channel3)),3] = cleanize(channel3)
	#channel_data_matrix[0:len(cleanize(channel4)),4] = cleanize(channel4)
	#channel_data_matrix[0:len(cleanize(channel5)),5] = cleanize(channel5)
	#channel_data_matrix[0:len(cleanize(channel6)),6] = cleanize(channel6)
	#channel_data_matrix[0:len(cleanize(channel7)),7] = cleanize(channel7)
	#channel_data_matrix[0:len(cleanize(channel8)),8] = cleanize(channel8)

	channel_data_intermed = np.matrix(channel_data_matrix)
	#channel_data_intermed = channel_data_matrix[0:len(cleanize(channel1)),:]


	#header_list = ['time', 'chan7', 'chan8', 'chan3', 'chan4', 'chan5', 'chan6', 'chan7', 'chan8', 'label']
	header_list = ['time', 'chan8', 'label']
	new_channel_data = pandas.DataFrame(channel_data_intermed, columns=header_list)
	new_channel_data.to_csv(new_file, sep=',', index=False)


#ONLY NEED TO CHANGE DIRECTORIES LISTED BELOW

set_label_and_clean('./SSVEP/2/label.txt', './SSVEP/2/data_main.txt', './SSVEP/2/new_data_main_33.txt')

