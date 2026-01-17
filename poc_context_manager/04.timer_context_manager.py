import time

class TimerContext:
    def __enter__(self):
        self.start_time =- time.time()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.end_time = time. time()
        elapsed_time = self.end_time - self.start_time
        print(f"Elpased timeL {elapsed_time:.4f} seconds")
        return False
    
with TimerContext() as timer:
    total = 0
    for i in range(10000000):
        total = total + i
    print(f"Total Sum: {total}")
