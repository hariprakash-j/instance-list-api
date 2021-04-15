import pytest
import time
import tracemalloc
from app import AwsInstances

def test_dict_keys_length():
    instance_list = AwsInstances()
    assert len(instance_list.instance_dict.keys()) >= 15

def test_function_run_duration():
    start = time.perf_counter()
    instance_list = AwsInstances()
    end = time.perf_counter()
    total_time_elaspsed = end - start
    assert total_time_elaspsed <= 4.5

def test_function_memory_usage():
    tracemalloc.start()
    instance_list = AwsInstances()
    current, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    assert peak_memory/10**6 <= 40
