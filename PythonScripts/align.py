import numpy as np
import pandas as pd

from scipy import signal
from sys import argv
from matplotlib import pyplot as plt

def errorFun(wave1, wave2):
	error = []

	for shift in range(-len(wave1) + 1, len(wave1)):
		error[shift] = 0
		for i, j in zip(range(len(wave1)), range(len(wave2) + shift)):
			if(j < len(wave2) or j < 0):
				error[shift] += (wave1[i] - wave2[j]) ** 2

	return error

def main(argv):
	wave_data = pd.read_csv(argv[1])
	x = wave_data["time"]
	y1 = wave_data["base sinewave"]
	y2 = wave_data["base cosine"]
	
	#plt.plot(x, y1, x, y2)
	
	dx = np.mean(np.diff(x))
	# shift = (np.argmax(signal.correlate(y1, y2)) - len(y1)) * dx
	shift = (np.argmin(errorFun(y1, y2)))
	plt.plot(x, y1, x + shift, y2)
	plt.show()
	
if __name__=="__main__":
	main(argv)