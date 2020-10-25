import multiprocessing as mp


class SharedEvents:
  def __init__(self):
    self.stop_event = mp.Event()
    self.init_event = mp.Event()
