# Tic Toc

It allows you to time some parts of your code in an easy way.

You can get it from pip.
```python
pip install ttictoc
```


# How to use it

First import the class
```python
from ttictoc import TicToc
```

Now, they are several ways to use it.

### Using the 'with' statement
Without creating any object you can time your code as follow.
```python
with TicToc('name'):
  some code...
  
# Prints the elapsed time
```

Or by creating an object you can do de same.
```python
t = TicToc()
with t:
  some code...
  
# Prints the elapsed time
```

### Calling tic toc explicitly
You can also call the tic toc explicitply as shown bellow.
```python
t = TicToc('name')
t.tic()
some code...
t.toc()
print(t.elapsed)
```
or
```python
t = TicToc()
t.tic()
some code...
print(t.toc())
```

### With indentation
If you want to time multiple levels of your code, you can also do it by setting 'indentation' to True.
```python
t = TicToc(indentation=True)
t.tic()
some code1...
t.tic()
some code2...
t.tic()
some code3...
print(t.toc()) # Prints time for code 3 
print(t.toc()) # Prints time for code 2 with code 3
print(t.toc()) # Prints time for code 1 with code 2 and 3
```

## Arguments
The class has 4 arguments: `name`,`method`,`indentation`, and `print_toc`. 
- `name`:  It's the name of the object. It's not required.
- `method`: Indicates which method should be used to get the time.
- `indentation`: Allows to use the same object several times, in different indentations to time.
- `print_toc`:  Indicate if you want to print, or not, the elapsed time when calling toc.

The `method` argument can be either `int`, `str`, or your method choice. If it's a string, the valid values are `time`, `perf_counter`, and `process_time`. If it's an integer, the valid values are `0`, `1`, and `2`. 
- `time` or `0`: time.time
- `perf_counter` or `1`: time.perf_counter
- `process_time` or `2`: time.process_time

If python version >= 3.7:
- `time_ns` or `3`: time.time_ns
- `perf_counter_ns` or `4`: time.perf_counter_ns
- `process_time_ns` or `5`: time.process_time_ns

In case you prefere to use other method you just do (using as example `time.clock`:
```python
TicToc(method=time.clock) 
```
