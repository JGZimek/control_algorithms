import unittest
import numpy as np
from utils.signal_utils import (
    generate_sin,
    generate_noise,
    generate_noise_signal,
    denoise_filter,
)


class TestSignalUtils(unittest.TestCase):
    """
    Unit tests for the signal utility functions in the utils.signal_utils module.
    """

    def test_generate_sin(self):
        """
        Test the generate_sin function.

        Ensures that the function generates the correct number of samples and
        that the lengths of the returned sine wave and x values match the expected size.
        """
        sin, x = generate_sin(1000, 6)
        self.assertEqual(len(sin), 1000)
        self.assertEqual(len(x), 1000)

    def test_generate_noise(self):
        """
        Test the generate_noise function.

        Verifies that the noise generated has the correct number of samples.
        """
        noise = generate_noise(1000, 0.1)
        self.assertEqual(len(noise), 1000)

    def test_generate_noise_signal(self):
        """
        Test the generate_noise_signal function.

        Ensures that the generated noise signal has the same length as the input
        signal and that the noise is correctly added to the signal.
        """
        signal = np.zeros(1000)
        noise = generate_noise(1000, 0.1)
        noisy_signal = generate_noise_signal(signal, noise)
        self.assertEqual(len(noisy_signal), 1000)
        self.assertTrue(np.all(noisy_signal == noise))

    def test_denoise_filter(self):
        """
        Test the denoise_filter function.

        Verifies that the denoised signal has the same length as the noisy input signal.
        """
        noisy_signal = np.random.randn(1000)
        denoised_signal = denoise_filter(noisy_signal, 10)
        self.assertEqual(len(denoised_signal), 1000)


if __name__ == "__main__":
    unittest.main()
