import numpy as np
import pandas as pd
import math

from scipy import signal
from sys import argv
from matplotlib import pyplot as plt

# Only works for similar waveforms and only gets kinda close
def libFun(wave1, wave2):
	mid = len(wave1)-1
	cor = np.correlate(wave1, wave2, 'full')
	return np.argmax(cor) - mid

def errorFun(wave1, wave2):
	wave_len = len(wave1)

	min_mse = math.inf
	min_shift = None

	for shift in range(-wave_len + 1, wave_len):
		# calculating upper and lower bound of shifted waveform
		lower_end = shift
		upper_end = lower_end + wave_len - 1

		if (upper_end >= 0 and lower_end < wave_len): # shifted wave contain points in base waveform's domain
			total_error = 0
			overlap = 0

			# calculating the total error for the shifted waveform
			if (upper_end < wave_len): # shifted wave inbound while its lower end out of bounds
				overlap = upper_end + 1
				for i in range(0, upper_end + 1):
					j = i - shift
					total_error += pow((wave2[j] - wave1[i]), 2)
			else: # shifted wave inbound while its upper end out of bounds
				overlap = wave_len - lower_end + 1
				for i in range(lower_end, wave_len):
					j = i - shift
					total_error += pow((wave2[j] - wave1[i]), 2)

			# calculating the mean of the SSE
			mse = total_error / overlap

			# tracking for min error
			if (mse < min_mse):
				min_mse = mse
				min_shift = shift

	return min_shift

def main(argv):
	wave_data = pd.read_csv(argv[1])
	x = wave_data["time"]
	y1 = wave_data["base sinewave"]
	y2 = wave_data["base cosine"]

	#plt.plot(x, y1, x, y2)

	dx = np.mean(np.diff(x))
	# shift = (np.argmax(signal.correlate(y1, y2)) - len(y1)) * dx
	plt.plot(x, y1, x, y2)
	# shift = errorFun(y1, y2) * dx
	shift = libFun(y1, y2) * dx
	print(shift)
	plt.plot(x, y1, x + shift, y2)
	plt.show()

if __name__=="__main__":
	main(argv)
