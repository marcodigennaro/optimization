import platform
import toml


def set_python_version():
    """
    Sets the Python version in the pyproject.toml file based on the operating system.
    """
    # Load the pyproject.toml file
    with open('pyproject.toml', 'r') as file:
        data = toml.load(file)

    # Check the operating system and set the Python version accordingly
    if platform.system() == 'Darwin':  # Darwin indicates macOS
        python_version = "^3.8"
    else:
        python_version = "^3.10"

    # Update the python version in the toml data
    data['tool']['poetry']['dependencies']['python'] = python_version

    # Save the updated pyproject.toml file
    with open('pyproject.toml', 'w') as file:
        toml.dump(data, file)


set_python_version()
