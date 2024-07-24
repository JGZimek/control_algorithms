import unittest
import numpy as np
from controllers.adaptive_control import AdaptiveController


class TestAdaptiveController(unittest.TestCase):
    """
    Unit tests for the AdaptiveController class in the controllers.adaptive_control module.
    """

    def setUp(self):
        """
        Set up the test environment for each test case.

        Initializes an AdaptiveController instance with a specified number of samples
        and signal length.
        """
        self.controller = AdaptiveController(1000, 6)

    def test_simulate(self):
        """
        Test the simulate method.

        Verifies that the simulate method returns the expected signal arrays
        (u_signal, v_signal, y_signal) and model parameters of correct lengths.
        This ensures the simulation function correctly generates the outputs.
        """
        u_signal, v_signal, y_signal, model_param, x, sin = self.controller.simulate(
            0.1, 1, 1, 1
        )
        self.assertEqual(len(u_signal), 1000)
        self.assertEqual(len(v_signal), 1000)
        self.assertEqual(len(y_signal), 1000)

    def test_identify(self):
        """
        Test the identify method.

        Ensures that the identify method correctly estimates the parameters
        based on the input and output signals. The test checks the shape of
        the estimated parameters and the parameter history to match expectations.
        """
        u_signal, v_signal, y_signal, _, _, _ = self.controller.simulate(0.1)
        estimated_param, param_hist = self.controller.identify(u_signal, y_signal, 1)
        self.assertEqual(estimated_param.shape, (3, 1))
        self.assertEqual(param_hist.shape, (3, len(y_signal)))


if __name__ == "__main__":
    unittest.main()
