# optimization

This repo provides a set of tutorials demonstrating different optimization problems and computational techniques to solve them.

## Getting Started

### Get the package

```
# Navigate to your local folder
cd /your/local/folder

# Clone the WindML repository
git clone git@github.com:marcodigennaro/optimization.git

# Enter the folder
cd optimization/

# Create the python environment from the pyproject.toml file
poetry install

# Activate the python environment
source .venv/bin/activate

# Run tests 
poetry run pytest -v

# Start Jupyter Lab
jupyter-lab  
```

### Content of the Jupyter Notebooks

  1. `bus_allocation.ipynb` presents a simple linear optimization problem and two main, non-trivial solutions. 
One is an educated guess coming from a common-sense hypothesis, the second one involve a simple linear optimization.
Both are compared to the real solution in terms of precision, memory and time required.

  2. `power_loss.ipynb` given an electrical power cable, whose diameter can change of 5cm, 
determine the optimal diameter such that the power losses due to the change in resistance is minimised, 
while ensuring the maximum current to be below the overheating limit. This uses the CPLEX library for advanced optimization.

### Author

Marco Di Gennaro 
- [My GitHub](https://github.com/marcodigennaro)
- [My Linkedin](https://www.linkedin.com/in/marcodig/)
- [My professional website](https://atomistic-modelling.com/)

### License

This project is licensed under the GPL v3 License - see the [LICENSE.md](https://github.com/marcodigennaro/WindML/blob/main/LICENSE.md) file for details

 
### Acknowledgements




