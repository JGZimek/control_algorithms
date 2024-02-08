import numpy as np
import matplotlib.pyplot as plt
from signal_tracking import SignalGenerator
from decorators_module import plot_generation_decorator


class MultilevelController:
    def __init__(self, samples_number, signal_length):
        self.signal_generator = SignalGenerator(samples_number, signal_length)

    def simulate(self, variance, a1=0.5, b1=1, a2=0.25, b2=1):
        model_param = np.array([[a1, b1], [a2, b2]])
        u_signal = np.array(
            [
                self.signal_generator.generate_noise(variance),
                self.signal_generator.generate_noise(variance),
            ]
        )
        noise = np.array(
            [
                self.signal_generator.generate_noise(variance),
                self.signal_generator.generate_noise(variance),
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

        # Least squares method
        estimated_param = [
            output_signal[0]
            @ input_matrix[0].T
            @ np.linalg.inv(input_matrix[0] @ input_matrix[0].T),
            output_signal[1]
            @ input_matrix[1].T
            @ np.linalg.inv(input_matrix[1] @ input_matrix[1].T),
        ]

        return estimated_param

    def control():
        pass

    @plot_generation_decorator
    def parameter_estimation_plot(
        self, input_signal, output_signal, model_param, connection_matrix
    ):
        estimated_param = self.identify(input_signal, output_signal, connection_matrix)
        labels = ["$a_1$", "$b_1$", "$a_2$", "$b_2$"]
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
        true, estimated, angles = (
            np.concatenate(
                (np.concatenate(model_param), [np.concatenate(model_param)[0]])
            ),
            np.concatenate(
                (np.concatenate(estimated_param), [np.concatenate(estimated_param)[0]])
            ),
            np.concatenate((angles, [angles[0]])),
        )
        _, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        (true_plot,) = ax.plot(
            angles,
            true,
            "b",
            alpha=0.7,
            label="True Values",
            marker="o",
        )
        (estimated_plot,) = ax.plot(
            angles,
            estimated,
            "r",
            alpha=0.7,
            label="Estimated Values",
            marker="o",
        )

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.set_rlabel_position(90)
        ax.set_rticks(
            np.arange(
                0,
                max(np.max(model_param), np.max(estimated_param)) + 0.1,
                max(np.max(model_param), np.max(estimated_param)) / 5,
            ),
            labels=[
                f"{i:.2f}"
                for i in np.arange(
                    0,
                    max(np.max(model_param), np.max(estimated_param)) + 0.1,
                    max(np.max(model_param), np.max(estimated_param)) / 5,
                )
            ],
        )

        true_plot.set_label(f"True Values:\n{"".join(f"{label}: {value:.2f}\n" for label, value in zip(labels, true))}")
        estimated_plot.set_label(f"Estimated Values:\n{"".join(f"{label}: {value:.2f}\n" for label, value in zip(labels, estimated))}")
        ax.legend()

        plt.title("True and Estimated Model Parameters")
        plt.show()


def main():
    multilevel_controller = MultilevelController(1000, 6)
    u_signal, v_signal, y_signal, model_param, connection_matrix = (multilevel_controller.simulate(1))
    multilevel_controller.parameter_estimation_plot(u_signal, y_signal, model_param, connection_matrix)


if __name__ == "__main__":
    main()
