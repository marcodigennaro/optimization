import time
from memory_profiler import memory_usage

def performance_measure(func):
    def wrapper(*args, **kwargs):
        # Measure memory just before function execution
        mem_start = memory_usage(max_usage=True)
        start_time = time.time()

        # Execute the function and store the result
        func_result = func(*args, **kwargs)

        end_time = time.time()
        # Measure memory immediately after function execution
        mem_end = memory_usage(max_usage=True)

        execution_time = end_time - start_time
        mem_usage = mem_end - mem_start  # Calculate the difference in memory usage

        # Extend the result with performance data if it's a dictionary
        print('func_result')
        print(func_result)
        func_result.update({
                'execution_time': execution_time,
                'memory_usage': mem_usage
        })

        return func_result

    return wrapper


def print_output(func):
    def wrapper(*args, **kwargs):
        # Execute the function and store the result
        out_dict = func(*args, **kwargs)
        print('out inisde print-out')
        print(out_dict)
        print(f"We need {out_dict['num_buses_A']} buses A")
        print(f"We need {out_dict['num_buses_B']} buses B")
        print(f"We need {out_dict['num_buses_C']} buses C")
        print(f"Minimum total cost: {out_dict['minimum_total_cost']}€")

        return out_dict

    return wrapper
