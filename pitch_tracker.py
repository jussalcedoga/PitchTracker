import crepe
from scipy.io import wavfile 
import numpy 
import click 
from matplotlib import pyplot

@click.command()
@click.option("-file", default = "bass.wav")

def main(file):

	time_ = list()
	frequency_ = list()
	confidence_ = list()

	sr, audio = wavfile.read(file)
	time, frequency, confidence, activation = crepe.predict(audio, sr, viterbi=True)

	time_ = time
	frequency_ = frequency
	confidence_ = 100*confidence

	filename = "{}".format(file.replace(".wav", ".dat"))
	outsample = open(filename, mode="w")
	outsample.write("{} {} {} \n".format("time", "frecuency", "% confidence"))

	for i, t in enumerate(time):
		outsample.write("{:.5f} {:.5f} {:.5f} \n".format(time_[i], frequency_[i], confidence_[i]))

	frequency_ = numpy.array(frequency_)
	mean_frecuency = numpy.mean(frequency_[0:len(frequency_)-10])
	outsample.write("The mean frecuency is: {} Hz".format(mean_frecuency))

	time = numpy.array(time_)
	frequency = numpy.array(frequency_)
	pyplot.figure()
	pyplot.plot(time[0:len(frequency)-10], frequency[0:len(frequency)-10], "-*", color = "crimson", label = r"$\langle f \rangle = %f \ \rm{Hz}$"%mean_frecuency)
	pyplot.ylabel(r"$f \ [\rm{Hz}]$", fontsize = 20)
	pyplot.xlabel(r"$time \ [s]$", fontsize = 20)
	pyplot.legend(loc = "best")
	pyplot.grid()
	pyplot.savefig("{}".format(filename.replace(".dat", ".pdf")))
	outsample.close()

if __name__ == '__main__':
	main()

