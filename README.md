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

# Set your operating system (MacOS vs Linux)
python python set_python_version.py

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

1. `bus_allocation` presents a simple linear optimization problem and two main, non-trivial solutions. 
One is an educated guess coming from a common-sense hypothesis, the second one involve a simple linear optimization.
Both are compared to the real solution in terms of precision, memory and time required.
2. `optimal_power_flow` Minimize the total generation cost of electrical power across several generating units while meeting fixed power demand and adhering to system stability constraints.
3. `power_loss` Determine the optimal wire diameter so that the power losses due to resistance is minimised while ensuring that the cable can carry a specified maximum current without overheating
4. `renewable_energy_flow` We need to optimize the distribution of energy from multiple sources to different consumers to minimize the overall cost, while satisfying demand constraints.

![Distribution of solutions for wind/solar production](https://github.com/marcodigennaro/optimization/blob/main/optimization/images/renewables.jpeg)

### Author

Marco Di Gennaro 
- [CV](https://github.com/marcodigennaro/CV/blob/main/MDG_CV.pdf)
- [GitHub](https://github.com/marcodigennaro)
- [Linkedin](https://www.linkedin.com/in/marcodig/)
- [professional website](https://atomistic-modelling.com/)

### License

This project is licensed under the GPL v3 License - see the [LICENSE.md](https://github.com/marcodigennaro/WindML/blob/main/LICENSE.md) file for details

