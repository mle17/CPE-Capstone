import numpy as np
import pandas as pd
import math

from scipy import signal
from sys import argv
from matplotlib import pyplot as plt

def errorFun(wave1, wave2):
	error = {}
	wave_len = len(wave1)

	for shift in range(-wave_len + 1, wave_len):

		# calculating upper and lower bound of shifted waveform
		lower_end = shift
		upper_end = lower_end + wave_len - 1

		if (upper_end >= 0 and lower_end < wave_len): # shifted wave contain points in base waveform's domain
			error[shift] = 0
			overlap = 0

			# calculating the total error for the shifted waveform
			if (upper_end < wave_len): # shifted wave inbound while its lower end out of bounds
				overlap = upper_end + 1
				for i in range(0, upper_end + 1):
					j = i - shift
					error[shift] += pow((wave2[j] - wave1[i]), 2)
			else: # shifted wave inbound while its upper end out of bounds
				overlap = wave_len - lower_end + 1
				for i in range(lower_end, wave_len):
					j = i - shift
					error[shift] += pow((wave2[j] - wave1[i]), 2)

			# calculating the mean of the SSE
			error[shift] = error[shift]/overlap

	return error

def main(argv):
	wave_data = pd.read_csv(argv[1])
	x = wave_data["time"]
	y1 = wave_data["base sinewave"]
	y2 = wave_data["base cosine"]

	#plt.plot(x, y1, x, y2)

	dx = np.mean(np.diff(x))
	# shift = (np.argmax(signal.correlate(y1, y2)) - len(y1)) * dx
	err_dict = errorFun(y1, y2)
	plt.plot(x, y1, x, y2)
	shift = min(err_dict, key=err_dict.get) * dx
	plt.plot(x, y1, x + shift, y2)
	plt.show()

if __name__=="__main__":
	main(argv)
