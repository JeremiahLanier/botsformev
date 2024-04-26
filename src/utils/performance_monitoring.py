import time


class PerformanceMonitor:
    def __init__(self):
        self.start_time = time.time()

    def log_performance(self):
        elapsed_time = time.time() - self.start_time
        print(f"Elapsed time: {elapsed_time} seconds")
