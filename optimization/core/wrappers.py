import time
import tracemalloc


def time_measure(func):
    """
    Decorator that measures the execution time of a function.

    Args:
        func (function): The function to be wrapped by the decorator.

    Returns:
        function: A wrapped function that, when called, adds the execution time to its returned dictionary.
    """

    def wrapper(*args, **kwargs):
        # Start timing
        start_time = time.time()

        # Execute the function
        result = func(*args, **kwargs)

        # Stop timing and calculate elapsed time
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Add execution time to the result dictionary
        result['elapsed_time'] = elapsed_time
        return result

    return wrapper


def performance_measure(func):
    """
    Decorator that measures memory usage of the function execution and adds it to the returned dictionary.

    Args:
        func (function): The function to be wrapped by the decorator.

    Returns:
        function: A wrapped function that, when called, adds the memory usage statistics (current and peak) to its result dictionary.
    """

    def wrapper(*args, **kwargs):
        # Start memory tracking
        tracemalloc.start()

        # Execute the function
        result = func(*args, **kwargs)

        # Get memory usage statistics
        current, peak = tracemalloc.get_traced_memory()

        # Stop memory tracking
        tracemalloc.stop()

        # Add memory usage to the result dictionary
        result['current'] = current
        result['peak'] = peak
        return result

    return wrapper


def print_output(func):
    """
    Decorator that prints formatted output from the result of a function.

    Args:
        func (function): The function to be wrapped by the decorator.

    Returns:
        function: A wrapped function that, when called, prints specific details from its returned dictionary and then returns the dictionary unchanged.
    """

    def wrapper(*args, **kwargs):
        # Execute the function and capture the result
        result = func(*args, **kwargs)

        # Print formatted output based on the function's result
        print(f"We need {result['A']} buses A")
        print(f"We need {result['B']} buses B")
        print(f"We need {result['C']} buses C")
        print(f"Minimum total cost: {result['minimum_total_cost']}€")

        return result

    return wrapper
