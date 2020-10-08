import pyaudio as pa
import signal

rate = 48000
fpb = 2048 #frames per buffer

p = pa.PyAudio()

#open input stream from MATRIX Voice
#input device 14 is the beamformed input from the MATRIX Voice
input_stream = p.open(format = pa.paInt16,
			   channels = 1,
			   rate = rate,
			   input=True,
			   frames_per_buffer = fpb,
			   input_device_index=14);

#open default output stream (the analog output) as mono
output_stream = p.open(format = pa.paInt16,
                       channels = 1,
                       rate = rate,
                       output=True,
                       frames_per_buffer = fpb)

#close streams on interrupt
def interrupt_handler(signum, sigframe):
	input_stream.stop_stream()
	output_stream.stop_stream()
	
	input_stream.close()
	output_stream.close()
	
	p.terminate()
	exit(0)
signal.signal(signal.SIGINT, interrupt_handler)

#playback the matrix voice input on the analog output
while True:
	beamformed = input_stream.read(fpb, exception_on_overflow=False)
	output_stream.write(beamformed)

