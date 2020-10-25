import alsaaudio as aa
import time

from .Component import Component


#class that plays audio to the default audio device
#should be raspberry pi aux output
class AuxSink(Component):
  def __init__(self, shared_events=None, frames_per_buffer=128, rate=48000):
    super().__init__(shared_events, source=False, sink=True);
    self.fpb = frames_per_buffer
    self.rate = rate
  
  def target(self):
    #open default output stream (the analog output) as mono
    output_stream = aa.PCM(type=aa.PCM_PLAYBACK, mode = aa.PCM_NONBLOCK,
                          rate = self.rate, channels=1, format = aa.PCM_FORMAT_S16_LE,
                          periodsize=self.fpb);
    
    #play audio until told to stop
    while True:
      if self.events.stop_event.is_set():
        break
      
      samples = self.pull_in()
      output_stream.write(samples) #non-blocking write. puts audio in some
                                   #internal buffer or something like that
