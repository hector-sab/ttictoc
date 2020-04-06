# ttictoc
Time execution of blocks of code.

## TocToc
The easiest way to time something is with `tic` and `toc`

```python
import time
from ttictoc import tic,toc
tic()
time.sleep(1)
elapsed = toc()
print('Elapsed time:',elapsed)
```

You can execute multiple tocs in a matlab-like fashon
```
import time
from ttictoc import tic,toc
tic()
for i in range(2):
  tic()
  time.sleep(1)
  elapsed = toc()
  print('[IN LOOP] Elapsed time:',elapsed)
print('[OUT LOOP] Elapsed time:',toc())
```

## Timer Class
It works just like `tic`,`toc`.
```python
import time
from ttictoc import Timer

# Simple
t = Timer()
t.start()
time.sleep(1)
elapsed = t.stop()
print('Elapsed time:',elapsed)


# Nested
t.start()
for i in range(2):
  t.start()
  time.sleep(1)
  elapsed = t.stop()
  print('[IN LOOP] Elapsed time:',elapsed)
print('[OUT LOOP] Elapsed time:',t.stop())
```

## Context manager
You can also use it as context manager
```python
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

## Deactivating matlab-like nesting
You can deactivate the matlab-like nesting. In this case calling start will update the global starting time for toc. However, you can have nested tics by giving a `key` to start and stop.
```python
import time
from ttictoc import Timer,tic2,toc2

tic()
for i in range(2):
  tic()
  time.sleep(1)
  elapsed = toc()
  print('[IN LOOP] Elapsed time:',elapsed)
print('[OUT LOOP] Elapsed time:',toc())

t = Timer(matlab_like=False)
t.start()
time.sleep(1)
t.start() # Restarts the starting point
time.sleep(1)
elapsed = t.stop()
print('Elapsed time:',elapsed) # ~1 second

# Nested
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
```

## Specify timing method
By default, `Timer` (and `tic`,`toc`) use `timeit.default_timer`. However, the timing function can be selected as follow.
```python
import time
from ttictoc import Timer
t = Timer(func_time=time.clock)
t.start()
time.sleep(5)
elapsed = t.stop()
print('Elapsed time:',elapsed)
```
