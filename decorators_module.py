def plot_generation_decorator(func):
        def wrapper(*args, **kwargs):
            print("In progress: generating the plot...")
            result = func(*args, **kwargs)
            print("Plot generated successfully.")
            return result

        return wrapper