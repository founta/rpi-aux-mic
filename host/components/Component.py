import multiprocessing as mp
from multiprocessing import SimpleQueue
from queue import Empty

class Component:
  def __init__(self, shared_events, source=False, sink=False):
    self.events = shared_events
    self.source = source
    self.sink = sink
    self.process = None
    
    if sink:
      self.data_out = None
    else:
      self.data_out = SimpleQueue()
    self.data_in = None
  
  def target(self):
    pass
  
  def set_shared_events(self, shared_events):
    self.events = shared_events
  
  def set_data_in(self, data_in):
    self.data_in = data_in
  
  def get_data_out(self):
    return self.data_out
  
  def pull_in(self, retry=0.0001):
    try:
      inp = self.data_in.get()
      return inp
    except Empty:
      time.sleep(retry)
  
  def put_out(self, out):
    self.data_out.put(out)
  
  def launch(self):
    self.process = mp.Process(target=self.target)
    self.process.start();
  
  def join(self):
    self.process.join()
