"""_summary_

Common Use Cases of Line-by-Line Processing:

01. Log File Analysis: 
    Efficiently scan large log files for patterns, errors, or metrics without loading
    the entire file into memory.
    
02. Data Processing Pipelines:
    Handle large datasets (e.g., CSV, JSON logs) by processing data incrementally,
    ideal for batch processing or real-time transformations.

03. Large Text Files:
    Process huge text files, such as datasets or raw data, while keeping memory usage low.

04. File Transformation:
    Read, transform, or filter data line by line, and write to another file without memory
    overload.

05. Streaming Data:
    Work with continuous data streams (e.g., log monitoring, real-time data pipelines) by
    processing each line as it comes without preloading everything.

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
