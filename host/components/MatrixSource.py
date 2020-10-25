import alsaaudio as aa

from .Component import Component


#class that reads beamformed audio channel from the matrix voice
class MatrixSource(Component):
  def __init__(self, shared_events=None, frames_per_buffer=128, rate=48000):
    super().__init__(shared_events, source=True, sink=False);
    self.fpb = frames_per_buffer
    self.rate = rate
  
  def target(self):
    #open input stream from MATRIX Voice
    #channel_8 is the beamformed input from the MATRIX Voice
    input_stream = aa.PCM(type=aa.PCM_CAPTURE, mode = aa.PCM_NORMAL,
                          rate=self.rate, channels=1, format=aa.PCM_FORMAT_S16_LE,
                          device="channel_8", periodsize=self.fpb);
    
    #read audio until program end
    while True:
      if self.events.stop_event.is_set():
        break
      (length, data) = input_stream.read() #blocking read
      self.put_out(data)
