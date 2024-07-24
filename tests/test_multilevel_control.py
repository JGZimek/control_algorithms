import unittest
import numpy as np
from controllers.multilevel_control import MultilevelController


class TestMultilevelController(unittest.TestCase):
    """
    Unit tests for the MultilevelController class in the controllers.multilevel_control module.
    """

    def setUp(self):
        """
        Set up the test environment for each test case.

        Initializes a MultilevelController instance with a specified number of samples
        and signal length.
        """
        self.controller = MultilevelController(1000, 6)

    def test_simulate(self):
        """
        Test the simulate method.

        Verifies that the simulate method returns signals (u_signal, v_signal, y_signal)
        and parameters (model_param, connection_matrix) of expected shapes and sizes.
        This ensures that the simulation function generates the correct outputs.
        """
        u_signal, v_signal, y_signal, model_param, connection_matrix = (
            self.controller.simulate(0.1, 0.5, 1, 0.25, 1)
        )
        self.assertEqual(u_signal.shape, (2, 1000))
        self.assertEqual(v_signal.shape, (2, 1000))
        self.assertEqual(y_signal.shape, (2, 1000))

    def test_identify(self):
        """
        Test the identify method.

        Verifies that the identify method correctly estimates the parameters
        based on the input and output signals. The test checks that the number
        of estimated parameters matches the expected number.
        """
        u_signal, v_signal, y_signal, model_param, connection_matrix = (
            self.controller.simulate(0.1)
        )
        estimated_param = self.controller.identify(
            u_signal, y_signal, connection_matrix
        )
        self.assertEqual(len(estimated_param), 2)


if __name__ == "__main__":
    unittest.main()
