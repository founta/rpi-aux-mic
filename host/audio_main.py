import signal
import time

from Pipeline import Pipeline
from components.all import MatrixSource, AuxSink


#TODO config file to define pipeline structure along with rate, frames per buffer
if __name__ == "__main__":
  rate = 48000
  fpb = 128
  
  #create the audio pipeline, just echos input from MATRIX Voice for now
  audio_pipeline = Pipeline()
  
  audio_pipeline.add(MatrixSource(rate=rate, frames_per_buffer=fpb))
  audio_pipeline.add(AuxSink(rate=rate, frames_per_buffer=fpb))
  
  #start the audio pipeline
  audio_pipeline.start()
  
  print("Pipeline started...")
  
  
  #set up interrupt handling
  def interrupt_handler(signum, sigframe):
    audio_pipeline.stop()
    print("Pipeline stopped!")
    exit(0)
  signal.signal(signal.SIGINT, interrupt_handler)
  
  #now wait until program exit
  while True:
    try:
      time.sleep(0.1)
    except KeyboardInterrupt:
      interrupt_handler(0,0)
