import numpy as np
from utils.signal_utils import generate_noise, generate_sin, generate_noise_signal


class AdaptiveController:
    """
    Class for adaptive control system simulation and parameter identification.
    """

    def __init__(self, samples_number, signal_length):
        """
        Initialize the AdaptiveController.

        Args:
            samples_number (int): Number of samples.
            signal_length (int): Length of the signal.
        """
        self.samples_number = samples_number
        self.signal_length = signal_length

    def simulate(self, variance, a0=1, a1=2, a2=3):
        """
        Simulate the adaptive control system.

        Args:
            variance (float): Variance of the noise.
            a0 (float): Parameter a0.
            a1 (float): Parameter a1.
            a2 (float): Parameter a2.

        Returns:
            tuple: u_signal, v_signal, y_signal, model_param, x, sin
        """
        sin, x = generate_sin(self.samples_number, self.signal_length)
        model_param = np.array([a0, a1, a2])

        u_signal = generate_noise(self.samples_number, variance)
        v_signal = np.convolve(u_signal, model_param, mode="full")[: len(u_signal)]
        noise = generate_noise(self.samples_number, variance)
        y_signal = generate_noise_signal(v_signal, noise)

        return u_signal, v_signal, y_signal, model_param, x, sin

    def identify(self, input_signal, output_signal, forgetting_factor):
        """
        Identify model parameters using recursive least squares.

        Args:
            input_signal (ndarray): Input signal.
            output_signal (ndarray): Output signal.
            forgetting_factor (float): Forgetting factor for the algorithm.

        Returns:
            tuple: estimated_param, param_hist
        """
        estimated_param = np.zeros((3, 1))
        weight_function = np.eye(3) * 10**3
        param_hist = np.zeros((3, len(output_signal)))

        regressor_vector = np.vstack(
            [
                np.array([input_signal[i], input_signal[i - 1], input_signal[i - 2]])
                for i in range(2, len(input_signal))
            ]
        )

        regressor_vector = np.vstack(
            [
                [input_signal[1], input_signal[0], 0],
                [input_signal[0], 0, 0],
                regressor_vector,
            ]
        )

        for i in range(len(output_signal)):
            rv_n = regressor_vector[i].reshape(-1, 1)
            weight_function = (1 / forgetting_factor) * (
                weight_function
                - (weight_function @ rv_n @ rv_n.T @ weight_function)
                / (forgetting_factor + rv_n.T @ weight_function @ rv_n)
            )
            estimated_param = estimated_param + weight_function @ rv_n @ (
                output_signal[i] - rv_n.T @ estimated_param
            )
            param_hist[:, i] = estimated_param.flatten()

        return estimated_param, param_hist
