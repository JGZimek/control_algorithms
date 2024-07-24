import numpy as np
from utils.signal_utils import generate_noise, generate_noise_signal


class MultilevelController:
    """
    Class for multilevel control system simulation and parameter identification.
    """

    def __init__(self, samples_number, signal_length):
        """
        Initialize the MultilevelController.

        Args:
            samples_number (int): Number of samples.
            signal_length (int): Length of the signal.
        """
        self.samples_number = samples_number
        self.signal_length = signal_length

    def simulate(self, variance, a1=0.5, b1=1, a2=0.25, b2=1):
        """
        Simulate the multilevel control system.

        Args:
            variance (float): Variance of the noise.
            a1 (float): Parameter a1.
            b1 (float): Parameter b1.
            a2 (float): Parameter a2.
            b2 (float): Parameter b2.

        Returns:
            tuple: u_signal, v_signal, y_signal, model_param, connection_matrix
        """
        model_param = np.array([[a1, b1], [a2, b2]])
        u_signal = np.array(
            [
                generate_noise(self.samples_number, variance),
                generate_noise(self.samples_number, variance),
            ]
        )
        noise = np.array(
            [
                generate_noise(self.samples_number, variance),
                generate_noise(self.samples_number, variance),
            ]
        )

        identity_matrix = np.eye(2)
        A = np.array([[a1, 0], [0, a2]])
        B = np.array([[b1, 0], [0, b2]])
        connection_matrix = np.array([[0, 1], [1, 0]])

        v_signal = np.linalg.inv(identity_matrix - A @ connection_matrix) @ B @ u_signal
        y_signal = (
            v_signal + np.linalg.inv(identity_matrix - A @ connection_matrix) @ noise
        )

        return u_signal, v_signal, y_signal, model_param, connection_matrix

    def identify(self, input_signal, output_signal, connection_matrix):
        """
        Identify model parameters using least squares method.

        Args:
            input_signal (ndarray): Input signals.
            output_signal (ndarray): Output signals.
            connection_matrix (ndarray): Connection matrix.

        Returns:
            list: Estimated parameters.
        """
        x_estimated = np.array(
            [
                connection_matrix[0] @ output_signal,
                connection_matrix[1] @ output_signal,
            ]
        )
        input_matrix = np.array(
            [
                [x_estimated[0], input_signal[0]],
                [x_estimated[1], input_signal[1]],
            ]
        )

        estimated_param = [
            output_signal[0]
            @ input_matrix[0].T
            @ np.linalg.inv(input_matrix[0] @ input_matrix[0].T),
            output_signal[1]
            @ input_matrix[1].T
            @ np.linalg.inv(input_matrix[1] @ input_matrix[1].T),
        ]

        return estimated_param
