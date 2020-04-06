import time
from ttictoc import Timer
from ttictoc import tic,toc # Matlab-like tic toc
from ttictoc import tic2,toc2 # Non matlab-like tic toc
print('>>> Tic Toc')
print('\nSimple Tic Toc')
tic()
time.sleep(1)
elapsed = toc()
print('Elapsed time:',elapsed)

print('\nNested Tic Toc')
tic()
for i in range(2):
  tic()
  time.sleep(1)
  elapsed = toc()
  print('[IN LOOP] Elapsed time:',elapsed)
print('[OUT LOOP] Elapsed time:',toc())




print('\n>>>Using Timer class')
print('\nSimple')
t = Timer()
t.start()
time.sleep(1)
elapsed = t.stop()
print('Elapsed time:',elapsed)

print('\nNested')
t.start()
for i in range(2):
  t.start()
  time.sleep(1)
  elapsed = t.stop()
  print('[IN LOOP] Elapsed time:',elapsed)
print('[OUT LOOP] Elapsed time:',t.stop())





print('>>> Tic Toc, v2 (non matlab-like)')
print('\nSimple Tic Toc')
tic2()
time.sleep(1)
elapsed = toc2()
print('Elapsed time:',elapsed)

print('\nNested Tic Toc')
tic2()
for i in range(2):
  tic2()
  time.sleep(1)
  elapsed = toc2()
  print('[IN LOOP] Elapsed time:',elapsed)
print('[OUT LOOP] Elapsed time:',toc2())




print('\n>>>Using Timer class, v2 (non matlab-like)')
print('\nSimple')
t = Timer(matlab_like=False)
t.start()
time.sleep(1)
t.start() # Restarts the starting point
time.sleep(1)
elapsed = t.stop()
print('Elapsed time:',elapsed) # ~1 second

print('\nNested')
t.start(key='Init')
for i in range(2):
  t.start(key=i)
  time.sleep(1)
  elapsed = t.stop(key=i)
  print('[IN LOOP] Elapsed time:',elapsed)
print('[OUT LOOP] Elapsed time:',t.stop('Init'))


print('\n[OUT LOOP][Init] Elapsed time:',t.stop('Init'))
print('[OUT LOOP][0] Elapsed time:',t.stop(0))
print('[OUT LOOP][1] Elapsed time:',t.stop(1))
t.clear_timers() # Delete all the timers, only works in not matlab-like mode






print('\n>>>Context Manager')
# Default
print('\nDefault')
with Timer():
  time.sleep(1)

# With out verbose
print('\nVerbose OFF')
with Timer(verbose=False) as T:
  time.sleep(1)
print('Elapsed time:',T.elapsed)

# With default verbose message
print('\nCustom Verbose')
with Timer(verbose_msg=f'[User msg][{time.time()}] Elapsed time: {{}}'):
  time.sleep(1)
