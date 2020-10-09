import pyaudio as pa
import signal

import multiprocessing as mp
from multiprocessing import SimpleQueue
from queue import Empty

import time

rate = 48000
fpb = 2048 #frames per buffer

p = pa.PyAudio()

def input_target(audio_queue, stop_event):
  #open input stream from MATRIX Voice
  #input device 14 is the beamformed input from the MATRIX Voice
  input_stream = p.open(format = pa.paInt16,
           channels = 1,
           rate = rate,
           input=True,
           frames_per_buffer = fpb,
           input_device_index=14);
  
  #read audio until program end
  while True:
    if stop_event.is_set():
      input_stream.stop_stream()
      input_stream.close()
      break
    audio_queue.put(input_stream.read(fpb, exception_on_overflow=True))


def output_target(audio_queue, stop_event):
  #open default output stream (the analog output) as mono
  output_stream = p.open(format = pa.paInt16,
                         channels = 1,
                         rate = rate,
                         output=True,
                         frames_per_buffer = fpb)
  
  #play audio until told to stop. Hopefully can handle incoming audio rate
  while True:
    if stop_event.is_set():
      output_stream.stop_stream()
      output_stream.close()
      break
    try:
      samples = audio_queue.get_nowait()
      output_stream.write(samples)
    except Empty:
      time.sleep(0.001)

stop_event = mp.Event()
audio_queue = SimpleQueue()

#close streams on interrupt
def interrupt_handler(signum, sigframe):
  stop_event.set()
  
  p.terminate()
  exit(0)
signal.signal(signal.SIGINT, interrupt_handler)

#kick off processes
input_process = mp.Process(target=input_target, args=(audio_queue, stop_event))
output_process = mp.Process(target=output_target, args=(audio_queue, stop_event))

input_process.start()
output_process.start()

#wait for program end by interrupt
while True:
  try:
    time.sleep(0.1)
  except KeyboardInterrupt:
    interrupt_handler(0,0)
