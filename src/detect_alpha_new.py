#!/usr/bin/env python

import rospy
from openbci.msg import BCIuVolts
from std_msgs.msg import Int32
from std_msgs.msg import Bool

from stft_new import STFT
from movavg import MovAvg
import matplotlib.pyplot as plt
import numpy as np
import cPickle
from time import sleep


def SPM_features(data,domain,req_freq,width):
    new_mag = []
    new_angle = []
    mag = np.abs(data)
    angle = np.angle(data)
    for freq in req_freq:
        mag_agg = []
        angle_agg = []
        for i in range(0,len(mag)):
            if domain[i] >= (freq - width/2.) and  domain[i] <= (freq + width/2.):
                mag_agg.append(mag[i])
                angle_agg.append(angle[i])
        new_mag.append(sum(mag_agg)/float(len(mag_agg)))
        new_angle.append(sum(angle_agg)/float(len(angle_agg)))
    return new_mag#+new_angle
        
def SPM(channel_data, freq = 250):
    width = 0.5
    z = np.fft.rfft(channel_data) # FFT
    y = np.fft.rfftfreq(len(channel_data), d = 1./freq) # Frequency data
    #z = zscore(z)
    req_freq = [10,12,15]#np.arange(2,25,width)
    return SPM_features(z,y,req_freq,width)

def make_features(channel_data):
    return SPM(channel_data)

class Ignore():
    def __init__(self, count):
        self.reset(count)

    def test(self):
        if self.count > 0:
            self.count -= 1
            return True
        else:
            return False

    def reset(self, count):
        self.count = count

class DetectAlpha():
    def __init__(self):
        with open('/home/siddarthkaki/new_ws/src/denoising/src/LR_classifier.pkl', 'rb') as fid:
            self.clf = cPickle.load(fid)
        # Initialize node
        rospy.init_node('detect_alpha', anonymous=True)

        # Get ros parameters
        sleep(5)
        fs = rospy.get_param("sampling_rate")
        channel_count = rospy.get_param("eeg_channel_count")

        # Initialize STFT
        self.stft = STFT(fs, 1.0, 1.0, channel_count)
        self.stft.remove_dc()
        self.stft.bandpass(5.0, 25.0)
        self.stft.window('hann')
        self.freq_bins = self.stft.freq_bins
        self.FFT = np.zeros((len(self.freq_bins), channel_count))

        # Choose channels
        self.channel_mask = np.full(channel_count, False, dtype = bool)
        self.channel_mask[7 -1] = True
        self.channel_mask[8 -1] = True

        # Define bands
        self.G1_mask = np.logical_and(5 < self.freq_bins, self.freq_bins < 7.5)
        self.Al_mask = np.logical_and(8.5 < self.freq_bins, self.freq_bins < 11.5)
        self.G2_mask = np.logical_and(12.5 < self.freq_bins, self.freq_bins < 15)

        # Initialize filters
        self.movavg = MovAvg(4)
        self.ignore = Ignore(0)

        self.pub_eyes = rospy.Publisher('classification', Int32, queue_size=1)

        # Subscribe
        rospy.Subscriber("reset_clf", Bool, self.subs)
        # self.subc = rospy.Subscriber("eeg_channels", BCIuVolts, self.newSample)

    def subs(self, msg):
        self.subc = rospy.Subscriber("eeg_channels", BCIuVolts, self.newSample)


    def newSample(self, msg):
        newFFT = self.stft.ingestSample(msg.data)
        if newFFT is not None:
            self.FFT = newFFT

            observation = [newFFT[:,6], newFFT[:,7]]
            observation = map(make_features,observation)
            observation = np.array(observation)
            shape = np.shape(observation)
            # data = data_
            observation = observation.reshape(1,-1)

            label = self.clf.predict(observation)
                
            # Publish messages

            self.pub_eyes.publish(label)
            self.subc.unregister()

    def updatePlot(self, line):
        line.set_ydata(np.sum(self.FFT[:,self.channel_mask], axis = 1))
        line.figure.canvas.draw()

if __name__ == '__main__':
    try:

        node = DetectAlpha()

        # fig, ax = plt.subplots()
        # li, = ax.plot(node.freq_bins, np.linspace(0, 10, len(node.freq_bins)))
        # ax.set_xlim([0, 40])
        # timer = fig.canvas.new_timer(interval=100)
        # timer.add_callback(node.updatePlot, li)
        # timer.start()
        # plt.show()

        rospy.spin()
    except rospy.ROSInterruptException:
        pass