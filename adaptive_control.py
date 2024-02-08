import numpy as np
import matplotlib.pyplot as plt
from signal_tracking import SignalGenerator
from decorators_module import plot_generation_decorator


class AdaptiveController:
    def __init__(self, samples_number, signal_length):
        self.signal_generator = SignalGenerator(samples_number, signal_length)

    def simulate(self, variance, a0=1, a1=2, a2=3):
        sin, x = self.signal_generator.generate_sin()
        model_param = np.array([a0, a1, a2])

        u_signal = self.signal_generator.generate_noise(variance)
        v_signal = np.convolve(u_signal, model_param, mode="full")[: len(u_signal)]
        noise = self.signal_generator.generate_noise(variance)
        y_signal = self.signal_generator.generate_noise_signal(v_signal, noise)

        return u_signal, v_signal, y_signal, model_param, x, sin

    def identify(self, input_signal, output_signal, forgetting_factor):
        estimated_param = np.zeros((3, 1))
        weight_function = np.zeros((3, 3))
        np.fill_diagonal(weight_function, 10**3)
        param_hist = np.zeros((3, len(output_signal), 1))

        # Creating a regressor vector Φ
        regressor_vector = np.vstack(
            [
                np.array([input_signal[i], input_signal[i - 1], input_signal[i - 2]])
                for i in range(2, len(input_signal))
            ]
        )
        regressor_vector = np.vstack(
            [np.array([input_signal[1], input_signal[0], 0]), regressor_vector]
        )
        regressor_vector = np.vstack(
            [np.array([input_signal[0], 0, 0]), regressor_vector]
        )

        # Recursive least squares algorithm
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
            param_hist[:, i, :] = estimated_param

        return estimated_param, param_hist

    def control(self, expected_output, model_parameters):
        pass

    @plot_generation_decorator
    def parameter_estimation_plot(
        self, input_signal, output_signal, forgetting_factor, parameters
    ):
        _, [a0, a1, a2] = self.identify(input_signal, output_signal, forgetting_factor)
        a0_exp, a1_exp, a2_exp = [np.full(len(output_signal), i) for i in parameters]
        data = [a0, a1, a2, a0_exp, a1_exp, a2_exp]
        label_pairs = [
            ("$a_0$", "solid"),
            ("$a_1$", "solid"),
            ("$a_2$", "solid"),
            (None, "dashed"),
            (None, "dashed"),
            (None, "dashed"),
        ]
        for data, (label, ls) in zip(data, label_pairs):
            plt.plot(range(len(output_signal)), data, label=label, ls=ls)
        plt.title("Title")
        plt.grid(True)
        plt.legend()
        plt.show()


def main():
    adaptive_controller = AdaptiveController(1000, 6)
    u_signal, v_signal, y_signal, model_parameters, x, sin = (adaptive_controller.simulate(0.1, 1, 1, 1))
    adaptive_controller.parameter_estimation_plot(u_signal, y_signal, 1, model_parameters)


if __name__ == "__main__":
    main()
