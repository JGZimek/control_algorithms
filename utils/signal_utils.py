import numpy as np


def generate_sin(samples_number, signal_length):
    """
    Generate a sine wave signal.

    Args:
        samples_number (int): Number of samples in the signal.
        signal_length (int): Length of the signal in terms of periods of pi.

    Returns:
        tuple: sin, x
    """
    x = np.linspace(0, signal_length * np.pi, samples_number)
    sin = np.sin(x)
    return sin, x


def generate_noise(samples_number, variance):
    """
    Generate noise based on a given variance.

    Args:
        samples_number (int): Number of samples in the noise.
        variance (float): Variance of the noise.

    Returns:
        ndarray: The generated noise.
    """
    return (np.random.rand(samples_number) - 0.5) * np.sqrt(12 * variance)


def generate_noise_signal(signal, noise):
    """
    Add noise to a signal.

    Args:
        signal (ndarray): The original signal.
        noise (ndarray): The noise to be added.

    Returns:
        ndarray: The signal with added noise.
    """
    return signal + noise


def denoise_filter(noise_signal, time_horizon):
    """
    Apply a denoising filter to a noisy signal.

    Args:
        noise_signal (ndarray): The noisy signal.
        time_horizon (int): Time horizon for the denoising filter.

    Returns:
        ndarray: The denoised signal.
    """
    denoise_signal = np.array([np.nan] * time_horizon)
    for i in range(time_horizon, len(noise_signal)):
        denoise_signal = np.append(
            denoise_signal, np.mean(noise_signal[i - time_horizon : i])
        )
    return denoise_signal
