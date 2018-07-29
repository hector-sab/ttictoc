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

t = TicToc(nested=True)
t.tic()
t.tic()
t.tic()
t.toc()
t.toc()
t.toc()
print(t.elapsed)
"""
import sys
import time
import warnings

class TicToc(object):
  """
  Counts the elapsed time.
  """
  def __init__(self,name='',method='time',nested=False,print_toc=True):
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
    nested (bool): Allows to do tic toc with nested with a single object.
        If True, you can put several tics using the same object, and each toc will 
        correspond to the respective tic.
        If False, it will only register one single tic, and return the respective 
        elapsed time of the future tocs.
    print_toc (bool): Indicates if the toc method will print the elapsed time or not.
    """
    self.name = name
    self.nested = nested
    if self.nested:
      self.tstart = []
    else:
      self.tstart = None

    self.__print_toc = print_toc

    self.__vsys = sys.version_info

    self.__int2strl_py37 = ['time','perf_counter','process_time','time_ns','perf_counter_ns','process_time_ns']
    self.__str2mtd_py37 = {'time':[time.time,'s'],'perf_counter':[time.perf_counter,'s'],'process_time':[time.process_time,'s'],
    'time_ns':[time.time_ns,'ns'],'perf_counter_ns':[time.perf_counter_ns,'ns'],'process_time_ns':[time.process_time_ns,'ns']}

    self.__int2strl_py27 = ['time','perf_counter','process_time']
    self.__str2mtd_py27 = {'time':[time.time,'s'],'perf_counter':[time.perf_counter,'s'],'process_time':[time.process_time,'s']}
    
    if self.__vsys[0]>2 and self.__vsys[1]>=7:
      # If python version is greater or equal than 3.7
      methods_int2str = self.__int2strl_py37
      methods_str2fn = self.__str2mtd_py37
    else:
      # If python vesion is lower than 3.7
      methods_int2str = self.__int2strl_py27
      methods_str2fn = self.__str2mtd_py27

    if type(method) is not int or type(method) is not str:
      self.__get_time = method

    # Parses from integer to string
    if type(method) is int and method<len(methods_int2str):
      method = methods_int2str[method]
    elif type(method) is int and method>len(methods_int2str):
      self.__warning_value(method)
      method = 'time'

    # Parses from int to the actual timer
    if type(method) is str and method in methods_str2fn:
      self.__get_time = methods_str2fn[method][0]
      self.__measure = methods_str2fn[method][1]
    elif type(method) is str and method not in methods_str2fn:
      self.__warning_value(method)
      self.__get_time = time.time


  def __warning_value(self,item):
    msg = "Value '{0}' is not a valid option. Using 'time' instead.".format(item)
    warnings.warn(msg,Warning)

  def __enter__(self):
    if self.nested:
      self.tstart.append(self.__get_time())
    else:
      self.tstart = self.__get_time()

  def __exit__(self,type,value,traceback):
    self.tend = self.__get_time()
    if self.nested:
      self.elapsed = self.tend - self.tstart.pop()
    else:
      self.elapsed = self.tend - self.tstart
    
    if self.__print_toc:
      if self.name!='': name = '[{}] '.format(self.name)
      else: name = self.name

      print('{0}Elapsed time: {1} ({2})'.format(name,self.elapsed,self.__measure))

  def tic(self):
    """
    Defines the start of the timing.
    """
    if self.nested:
      self.tstart.append(self.__get_time())
    else:
      self.tstart = self.__get_time()

  def toc(self):
    """
    Defines the end of the timing.
    """
    self.tend = self.__get_time()
    if self.nested:
      if len(self.tstart)>0:
        self.elapsed = self.tend - self.tstart.pop() 
      else:
        self.elapsed = None
    else:
      if self.tstart:
        self.elapsed = self.tend - self.tstart
      else:
        self.elapsed = None

    if self.__print_toc:
      if self.name!='': name = '[{}] '.format(self.name)
      else: name = self.name

      print('{0}Elapsed time: {1} ({2})'.format(name,self.elapsed,self.__measure))

    return(self.elapsed)

  def set_print_toc(self,set_print):
    """
    Indicate if you want the timed time printed out or not.
    Args:
      set_print (bool): If True, a message with the elapsed time will be printed.
    """
    if type(set_print) is bool:
      self.__print_toc = set_print
    else:
      warnings.warn("Parameter 'set_print' not boolean. Ignoring the command.",Warning)