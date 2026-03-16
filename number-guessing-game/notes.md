## time

`time` is a built-in Python module for working with time.
```python
import time
```

### Common methods

| Method | Description | Example |
|--------|-------------|---------|
| `time.time()` | current time in seconds since 1970 (Unix timestamp) | `1741234567.89` |
| `time.sleep(n)` | pause execution for n seconds | `time.sleep(2)` |
| `time.localtime()` | current local time as a struct | `time.struct_time(...)` |
| `time.gmtime()` | current UTC time as a struct | `time.struct_time(...)` |
| `time.strftime(format)` | format struct time as string | `time.strftime("%H:%M:%S")` |
| `time.strptime(string, format)` | parse string into struct time | `time.strptime("12:30", "%H:%M")` |
| `time.mktime(struct)` | convert local struct time to timestamp | `time.mktime(time.localtime())` |
| `time.monotonic()` | clock that only moves forward, not affected by system time changes | `time.monotonic()` |
| `time.perf_counter()` | highest resolution timer, best for benchmarking | `time.perf_counter()` |
| `time.process_time()` | CPU time used by current process only | `time.process_time()` |
| `time.timezone` | offset of local time from UTC in seconds | `-18000` |
| `time.ctime(timestamp)` | convert timestamp to readable string | `"Sat Mar 14 17:30:00 2025"` |

### How we use it in the project
```python
start_time = time.time()            # save start timestamp
elapsed = time.time() - start_time  # subtract to get elapsed seconds
elapsed = round(elapsed, 2)         # round to 2 decimal places
```

---

## random

`random` is a built-in Python module for generating random values.
```python
import random
```

### Common methods

| Method | Description | Example |
|--------|-------------|---------|
| `random.randint(a, b)` | random integer between a and b inclusive | `random.randint(1, 100)` → `42` |
| `random.random()` | random float between 0.0 and 1.0 | `0.7312...` |
| `random.uniform(a, b)` | random float between a and b | `random.uniform(1.0, 10.0)` |
| `random.choice(seq)` | random element from a sequence | `random.choice([1, 2, 3])` |
| `random.choices(seq, weights, k)` | k random elements with repetition, supports weights | `random.choices([1,2,3], weights=[1,2,3], k=5)` |
| `random.shuffle(seq)` | shuffle a list in place | `random.shuffle([1, 2, 3])` |
| `random.sample(seq, k)` | k unique random elements from a sequence | `random.sample([1,2,3,4], 2)` |
| `random.seed(n)` | fix the random generator to get same sequence every time | `random.seed(42)` |
| `random.gauss(mu, sigma)` | random float with normal distribution | `random.gauss(0, 1)` |
| `random.expovariate(lambda)` | random float with exponential distribution | `random.expovariate(1.5)` |
| `random.randrange(start, stop, step)` | random integer from range with optional step | `random.randrange(0, 100, 5)` |
| `random.getrandbits(k)` | random integer with k random bits | `random.getrandbits(8)` |

### How we use it in the project
```python
number = random.randint(1, 100)  # random integer from 1 to 100 inclusive
```