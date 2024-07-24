import unittest
import numpy as np
from utils.plotter import unified_plot, radar_plot


class TestPlotter(unittest.TestCase):
    """
    Unit tests for the plotting functions in the utils.plotter module.
    """

    def test_unified_plot(self):
        """
        Test the unified_plot function.

        Verifies that the function can plot both sine and cosine functions
        without raising exceptions. This test checks the basic functionality
        of line plotting with labels and a title.
        """
        x = np.linspace(0, 10, 100)
        y = [np.sin(x), np.cos(x)]
        labels = ["sin(x)", "cos(x)"]
        try:
            unified_plot(x, y, labels, title="Test Plot")
        except Exception as e:
            self.fail(f"unified_plot raised an exception: {e}")

    def test_radar_plot(self):
        """
        Test the radar_plot function.

        Ensures that the radar plot function can visualize true and estimated
        values without raising exceptions. This test verifies the basic functionality
        of radar plotting with labels and a title.
        """
        true_values = [0.5, 0.7, 0.2, 0.3]
        estimated_values = [0.6, 0.6, 0.3, 0.4]
        labels = ["A", "B", "C", "D"]
        try:
            radar_plot(true_values, estimated_values, labels, title="Test Radar Plot")
        except Exception as e:
            self.fail(f"radar_plot raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()
