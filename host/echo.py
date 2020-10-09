#import pyaudio as pa

import alsaaudio as aa

import signal

import multiprocessing as mp
from multiprocessing import SimpleQueue
from queue import Empty

import time

rate = 48000
fpb = 48 #frames per buffer

def input_target(audio_queue, stop_event):
  #open input stream from MATRIX Voice
  #input device 14 is the beamformed input from the MATRIX Voice
  input_stream = aa.PCM(type=aa.PCM_CAPTURE, mode = aa.PCM_NORMAL,
                        rate = rate, channels=1, format = aa.PCM_FORMAT_S16_LE,
                        device="channel_8", periodsize=fpb);
  
  #read audio until program end
  while True:
    if stop_event.is_set():
      break
    (length, data) = input_stream.read()
    audio_queue.put(data)


def output_target(audio_queue, stop_event):
  #open default output stream (the analog output) as mono
  output_stream = aa.PCM(type=aa.PCM_PLAYBACK, mode = aa.PCM_NORMAL,
                        rate = rate, channels=1, format = aa.PCM_FORMAT_S16_LE,
                        periodsize=fpb);
  
  #play audio until told to stop. Hopefully can handle incoming audio rate
  while True:
    if stop_event.is_set():
      break
    try:
      samples = audio_queue.get()
      output_stream.write(samples)
    except Empty:
      time.sleep(0.001)

stop_event = mp.Event()
audio_queue = SimpleQueue()

#close streams on interrupt
def interrupt_handler(signum, sigframe):
  stop_event.set()
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
