"""_summary_
"""
import time
from memory_profiler import memory_usage

def read_file_generator(p_file_path):
    """_summary_

    Args:
        p_file_path (_type_): _description_

    Yields:
        _type_: _description_
    """
    with open(p_file_path, encoding='utf-8') as file:
        for line in file:
            yield line.strip()

def process_data(p_file_path):
    """_summary_

    Args:
        p_file_path (_type_): _description_
    """
    for _ in read_file_generator(p_file_path):
        pass

G_FILE_PATH = r"generators-vs-traditional_method/reading_large_file/test_file1.txt"

# Measure Time and Memory Usage
g_start_time = time.time()
mem_usage_traditional  = memory_usage((process_data, (G_FILE_PATH, )))
g_end_time = time.time()

#Show results
print(f"Generator Method: Memory Usage: {max(mem_usage_traditional)} MB")
print(f"Generator Method: Execution Time: {g_end_time - g_start_time} seconds")
# Generator Method: Memory Usage: 21.87890625 MB
# Generator Method: Execution Time: 0.03270864486694336 seconds
