# Control System Simulation and Analysis

## Overview

This project includes modules for simulating and analyzing control systems using adaptive and multilevel control algorithms. The project is organized into distinct modules, each responsible for different aspects of the system, including signal generation, noise addition, plotting, and core algorithms.

## Project Structure

- **/controllers**: Contains the core algorithm classes for adaptive and multilevel control systems.
- **/utils**: Utility functions and modules like signal generation, plotting, and decorators.
- **/cli**: Command-line interface scripts for running the project.
- **/tests**: Unit tests for different components of the project.
- **/docs**: Documentation, including the README and any additional project documentation.

## Getting Started

To get started with the project, follow these steps:

1. **Clone the Repository**:
   First, clone the repository from GitHub to your local machine using the command:

   ```bash
   git clone https://github.com/JGZimek/Control_systems.git
   cd Control_systems
   ```

2. **Create a Virtual Environment**:
   It's recommended to create a virtual environment to manage dependencies. Run the following commands:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\Activate`
   ```

3. **Install Dependencies**:
   Install the necessary dependencies listed in the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   You can now use the CLI to run the simulations and view the results as described in the Usage section.

## Usage

### Command-line Interface

You can use the CLI to run simulations and plot parameter estimations.

#### Adaptive Controller

To run the adaptive controller simulation, use the following command:

```bash
python run_cli.py adaptive --samples 1000 --length 6 --variance 0.1 --a0 1 --a1 1 --a2 1 --forgetting_factor 1
```

Parameters:

- `--samples`: Number of samples.
- `--length`: Length of the signal.
- `--variance`: Variance of the noise.
- `--a0`, `--a1`, `--a2`: Model parameters.
- `--forgetting_factor`: Forgetting factor for parameter identification.

#### Multilevel Controller

To run the multilevel controller simulation, use the following command:

```bash
python run_cli.py multilevel --samples 1000 --length 6 --variance 0.1 --a1 0.5 --b1 1 --a2 0.25 --b2 1
```

Parameters:

- `--samples`: Number of samples.
- `--length`: Length of the signal.
- `--variance`: Variance of the noise.
- `--a1`, `--b1`, `--a2`, `--b2`: Model parameters.

## Documentation

### AdaptiveController

Class for simulating and identifying parameters in adaptive control systems.

- **simulate**: Simulates the system with given parameters.
- **identify**: Identifies system parameters using recursive least squares.

### MultilevelController

Class for multilevel control system simulation and parameter identification.

- **simulate**: Simulates the system with multilevel control.
- **identify**: Identifies parameters using least squares method.

### Utility Functions

Provided in `utils/signal_utils.py` for signal generation and noise handling.

- `generate_sin(samples_number, signal_length)`: Generates a sine wave signal.
- `generate_noise(samples_number, variance)`: Generates noise based on the given variance.
- `generate_noise_signal(signal, noise)`: Adds noise to a signal.
- `denoise_filter(noise_signal, time_horizon)`: Applies a denoising filter to a noisy signal.

### Plotting

Provided in `utils/plotter.py` for unified and radar plots.

- `unified_plot(x, y, labels, title="", plot_type='line', xlabel="X", ylabel="Y")`: Creates a unified plot for line or scatter plots.
- `radar_plot(true_values, estimated_values, labels, title="")`: Creates a radar plot for comparing true and estimated values.

## Testing

Unit tests are provided in the `/tests` directory for different components of the project. To run the tests, use:

```bash
python -m unittest discover -s tests
```

## Contact

For any inquiries, please contact [jgzimek@gmail.com].
