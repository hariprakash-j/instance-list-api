import pytest
import time
import tracemalloc
from app import AwsInstances

# tests the api call , by checking if number of the regions returned by the call is equal or greater than 15
def test_dict_keys_length():
    instance_list = AwsInstances()
    assert len(instance_list.instance_dict.keys()) >= 15

# checks how long the program takes to run accounting for the overhead in lambda, as our lambda function is limited to 6 seconds
def test_function_run_duration():
    start = time.perf_counter()
    instance_list = AwsInstances()
    end = time.perf_counter()
    total_time_elaspsed = end - start
    assert total_time_elaspsed <= 4.5

# checks the memory usage of the program accounting for the overhead in lambda, as our lambda function is limited to 200 MB of memory
def test_function_memory_usage():
    tracemalloc.start()
    instance_list = AwsInstances()
    current, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    assert peak_memory/10**6 <= 40
