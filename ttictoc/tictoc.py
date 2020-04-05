"""
Time execution 

# How to use it:

## TicToc
The easiest way included here is using tic and toc
```
from ttictoc import tic,toc
tic() # Start timing
# some code
elapsed = toc() # Gets the elapsed time until this moment
print('Elapsed time:',elapsed)
```

You can execute multiple tocs and will be linked to the `tic` time.
Also, each time `tic` is executed the time holded by `tic` will be
updated.
```
import time
from ttictoc import tic,toc
tic() # Start timing
time.sleep(1)
tic() # Reset the starting time
time.sleep(1)
print(toc()) # Prints ~1 seconds
time.sleep(1)
print(toc()) # Prints ~2 seconds
```

## Timer Class
The Timer class can be used to have a single and multiple timers.
Examples seen with tic,toc are also valid with Timer start,stop
```
import time
from ttictoc import Timer

# General timer
t = Timer()
t.start() # Starts the general timer
time.sleep(1)
elapsed = t.stop()
print('Elapsed time:',elapsed)

# Multiple timers
t.start('t0')
for i in range(2):
  tname = 't'+str(i+1)
  t.start(tname)
  time.sleep(1)
  elapsed = t.stop(tname)
  print('[INSIDE LOOP][{}] Elapsed time: {}'.format(tname,elapsed))
t.stop('t0')

print('[OUTSIDE LOOP][{}] Elapsed time: {}'.format('t0',t.elapsed['t0']))
print('[OUTSIDE LOOP][{}] Elapsed time: {}'.format('t1',t.elapsed['t1']))
print('[OUTSIDE LOOP][{}] Elapsed time: {}'.format('t2',t.elapsed['t2']))
```

## Context manager
You can also use it as context manager
```
import time
from ttictoc import Timer

# Default
with Timer():
  time.sleep(1)

# With out verbose
with Timer(verbose=False) as T:
  time.sleep(1)
print('Elapsed time:',T.elapsed)

# With default verbose message
with Timer(verbose_msg=f'[User msg][{time.time()}] Elapsed time: {{}}'):
  time.sleep(1)
```
"""
import timeit

class TimerError(Exception):
  """A custom exception used to report errors in use of Timer class"""

def select_default_timing_method():
  """
  Recomended timer from python 3.3 onwards is
  `time.perf_counter` and it seems like timeit
  automatically selects it depending on your python
  version. 
  """
  #import sys
  # For python version 3.7+
  #v_major = sys.version_info[0]
  #v_minor = sys.version_info[1]
  
  return timeit.default_timer

class Timer:
  """Keep track of elapsed time"""
  def __init__(self,func_time=None,matlab_like=True,**kwargs):
    """
    - func_time (): Function used to time. For example `time.time`,
        `time.clock`, or `time.perf_counter_ns`.
    -matlab_like (bool): Nested loops work like in matlab.
    
    Extra args for context manager mode
    - verbose (bool): Print the elapsed time with a default msg
    - verbose_msg (str): Message printed as verbose. It should contain one
        `{}` to insert the elapsed time.
    """
    self.matlab_like = matlab_like
    self.kwargs = kwargs
    # General starting time
    self._start_time = None
    # Select method of choise for the timer
    self._get_time = select_default_timing_method()
    if func_time:
      self._get_time = func_time
    # Allow to save multiple timers
    self._timers_start = dict()
    self.elapsed = dict()
    if matlab_like:
      self._timers_start = []
      self.elapsed = None

  def start(self,key=None):
    """
    - key ()
    """
    if self.matlab_like:
      self._timers_start.append(self._get_time())
    else:
      if not key:
        self._start_time = self._get_time()
      else:
        self._timers_start[key] = self._get_time()

  def stop(self,key=None):
    # Get stopping time
    _stop_time = self._get_time()
    
    if self.matlab_like:
      if len(self._timers_start)==0:
        _elap_time = None
      else:
        _elap_time = _stop_time - self._timers_start.pop()
    else:
      # Handle initialization errors first
      if (not key and not self._start_time or
        key and not key in self._timers_start.keys()):
        raise TimerError(f"Timer is not running. Use .start() to start it")
      
      # Select correct starting time
      _start_time = self._start_time
      if key: _start_time = self._timers_start[key]
      
      # Calculate elapsed time
      _elap_time = _stop_time - _start_time
      if key: self.elapsed[key] = _elap_time

    return _elap_time

  def clear_timers(self):
    """Cleaer all start times if any"""
    if not self.matlab_like:
      self._timers_start = dict()
      self.timers_elapsed = dict()

  def __enter__(self):
    self.elapsed = None
    self._start_time = self._get_time()
    return self

  def __exit__(self,type,value,traceback):
    """
    - verbose (bool): Print elapsed time or not
    - verbose_msg (str): If present, change the text of the verbose
    """
    _stop_time = self._get_time()
    self.elapsed = _stop_time - self._start_time
    
    # Check for verbose flag
    if 'verbose' not in self.kwargs.keys(): verbose = True
    else: verbose = self.kwargs['verbose']
    # Check for user verbose text
    if 'verbose_msg' not in self.kwargs.keys(): verbose_msg = 'Elapsed time: {}'
    else: verbose_msg = self.kwargs['verbose_msg']

    if verbose:
      print(verbose_msg.format(self.elapsed))



# For tic toc
__TICTOC_HELPER_CLASS_asdfgqwerzxcv1234 = Timer(matlab_like=True)
tic = __TICTOC_HELPER_CLASS_asdfgqwerzxcv1234.start
toc = __TICTOC_HELPER_CLASS_asdfgqwerzxcv1234.stop


if __name__=='__main__':    # Get stopping time
  import time
  t = Timer(matlab_like=False)
  # Test Raise TimeError if stoped without start
  # Test Raise TimeError if double start
  # Test returned value of stop

  print('Starting...')
  t.start()
  t.start('1')
  time.sleep(1)
  t.start()
  time.sleep(1)
  print('Stopping...')
  elapsed = t.stop()
  elapsed1 = t.stop('1')
  print('Elapsed: ',elapsed)
  print('Elapsed1: ',elapsed1, type(elapsed1))
  print(t.elapsed)
  
  print('Using Context Manager 1')
  with Timer() as T:
    time.sleep(1)
  print('Using Context Manager 2')
  with Timer(verbose=False) as T:
    time.sleep(1)
  print('Elapsed time:',T.elapsed)
  print('Using Context Manager 3')
  with Timer(verbose_msg=f'[User msg][{time.time()}] Elapsed time: {{}}') as T:
    time.sleep(1)

  print('Using Tic Toc')
  tic()
  time.sleep(2)
  elapsed = toc()
  print('Elapsed time:',elapsed)

  print('Nested Tic Toc')
  tic()
  for i in range(2):
    tic()
    time.sleep(1)
    elapsed = toc()
    print('[IN] Elapsed:',elapsed)
  elapsed = toc()
  print('[OUT] Elapsed:',elapsed)
