from SharedEvents import SharedEvents

#a pipeline meant to aid in receiving/processing/playing audio
class Pipeline:
  def __init__(self):
    self.events = SharedEvents()
    self.components = []
  
  #adds a component to the pipeline
  def add(self, component):
    #basic error checking; first component has to produce data
    if len(self.components) == 0:
      if not component.source:
        raise RuntimeError("The first component in the pipeline must be a source! %s is not" 
                            % (type(component).__qualname__))
    else: #print warning if there are multiple sources
      if component.source:
        print("There are multiple sources in this pipeline, as %s is also a source!"
               % (type(component).__qualname__))
    
    self.components.append(component)
    self.components[-1].set_shared_events(self.events)
    
    #link the output of the previous component to the input of this one
    if not component.source:
      self.components[-1].set_data_in(self.components[-2].get_data_out())
  
  #tell each component to stop and to join their threads
  def stop(self):
    self.events.stop_event.set()
    for component in self.components:
      component.join()
  
  #launches each component thread
  def start(self):
    for component in self.components:
      component.launch()
