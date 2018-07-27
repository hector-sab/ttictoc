"""
Author: Hector Sanchez
Date: 2018-07-26
Description: Class that allows you to do 'tic toc' to your code.

This class was based the answers that you can find in the next url.
https://stackoverflow.com/questions/5849800/tic-toc-functions-analog-in-python

How to use it:

with TicToc('name'):
  some code....

or

t = TicToc('name')
t.tic()
some code...
t.toc()
print(t.elapsed)

or 

t = TicToc('name',time.clock) # or any other method. 
                             # time.clock seems to be deprecated
with t:
  some code....

or

t = TicToc(,indentation=True)
t.tic()
t.tic()
t.tic()
t.toc()
print(t.elapsed)
t.toc()
print(t.elapsed)
t.toc()
print(t.elapsed)
"""
import sys
import time

class TicToc(object):
  """
  Counts the elapsed time.
  """
  def __init__(self,name='',method='time',indentation=False):
    """
    Args:
    name (str): Just informative, not needed
    method (int|str|ftn|clss): Still trying to understand the default
        options. 'time' uses the 'real wold' clock, while the other
        two use the cpu clock. If you want to use your own method, do it
        through this argument

        Valid int values:
          0: time.time  |  1: time.perf_counter  |  2: time.proces_time
          
          if python version >= 3.7:
          3: time.time_ns  |  4: time.perf_counter_ns  |  5: time.proces_time_ns

        Valid str values:
          'time': time.time  |  'perf_counter': time.perf_counter
          'process_time': time.proces_time

          if python version >= 3.7:
          'time_ns': time.time_ns  |  'perf_counter_ns': time.perf_counter_ns  
          'proces_time_ns': time.proces_time_ns

        Others:
          Whatever you want to use as time.time
    indentation (bool): Allows to do tic toc with indentation with a single object.
        If True, you can put several tics using the same object, and each toc will 
        correspond to the respective tic.
        If False, it will only register one single tic, and return the respective 
        elapsed time of the future tocs.
    """
    self.name = name
    self.indentation = indentation
    if self.indentation:
      self.tstart = []

    self.__measure = 's' # seconds

    self.__vsys = sys.version_info

    if self.__vsys[0]>2 and self.__vsys[1]>=7:
      # If python version is greater or equal than 3.7
      if type(method) is int:
        if method==0: method = 'time'
        elif method==1: method = 'perf_counter'
        elif method==2: method = 'process_time'
        elif method==3: method = 'time_ns'
        elif method==3: method = 'perf_counter_ns'
        elif method==4: method = 'process_time_ns'
        else: 
          import warnings
          msg = "Value '{0}' is not a valid option. Using 'time' instead.".format(method)
          warnings.warn(msg,Warning)
          method = 'time'

      if type(method) is str:
        if method=='time': self.get_time = time.time
        elif method=='perf_counter': self.get_time = time.perf_counter
        elif method=='process_time': self.get_time = time.process_time
        elif method=='time_ns': self.get_time = time.time_ns, self.__measure = 'ns' # nanoseconds
        elif method=='perf_counter_ns': self.get_time = time.perf_counter_ns, self.__measure = 'ns' # nanoseconds
        elif method=='process_time_ns': self.get_time = time.process_time_ns, self.__measure = 'ns' # nanoseconds
        else: 
          import warnings
          msg = "Value '{0}' is not a valid option. Using 'time' instead.".format(method)
          warnings.warn(msg,Warning)
          self.get_time = time.time
      
      else:
        self.get_time = method
    else:
      # If python vesion is lower than 3.7
      if type(method) is int:
        if method==0: method = 'time'
        elif method==1: method = 'perf_counter'
        elif method==2: method = 'process_time'
        else: 
          import warnings
          msg = "Value '{0}' is not a valid option. Using 'time' instead.".format(method)
          warnings.warn(msg,Warning)
          method = 'time'

      if type(method) is str:
        if method=='time': self.get_time = time.time
        elif method=='perf_counter': self.get_time = time.perf_counter
        elif method=='process_time': self.get_time = time.process_time
        else: 
          import warnings
          msg = "Value '{0}' is not a valid option. Using 'time' instead.".format(method)
          warnings.warn(msg,Warning)
          self.get_time = time.time

      else:
        self.get_time = method

  def __enter__(self):
    if self.indentation:
      self.tstart.append(self.get_time())
    else:
      self.tstart = self.get_time()

  def __exit__(self,type,value,traceback):
    self.tend = self.get_time()
    if self.indentation:
      self.elapsed = self.tend - self.tstart.pop()
    else:
      self.elapsed = self.tend - self.tstart
    
    if self.name!='': name = '[{}] '.format(self.name)
    else: name = self.name

    print('{0}Elapsed time: {1} ({2})'.format(name,self.elapsed,self.__measure))

  def tic(self):
    if self.indentation:
      self.tstart.append(self.get_time())
    else:
      self.tstart = self.get_time()

  def toc(self):
    self.tend = self.get_time()
    if self.indentation:
      if len(self.tstart)>0:
        self.elapsed = self.tend - self.tstart.pop() 
      else:
        self.elapsed = None
    else:
      self.elapsed = self.tend - self.tstart
    return(self.elapsed)