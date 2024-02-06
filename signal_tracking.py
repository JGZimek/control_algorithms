import numpy as np
import matplotlib.pyplot as plt


class SignalGenerator:
    def __init__(self, samples_number, signal_length):
        self.samples_number = samples_number
        self.signal_length = signal_length

    def generate_sin(self):
        x = np.linspace(0, self.signal_length * np.pi, self.samples_number)
        sin = np.sin(x)
        return sin, x

    def generate_noise(self, variance):
        noise = (np.random.rand(self.samples_number) - 0.5) * np.sqrt(12 * variance)
        return noise

    def generate_noise_signal(self, signal, noise):
        return signal + noise

    def denoise_filter(self, noise_signal, time_horizon):
        denoise_signal = np.array([])
        for i in range(0, time_horizon):
            denoise_signal = np.append(denoise_signal, np.nan)
        for i in range(time_horizon, len(noise_signal)):
            denoise_signal = np.append(
                denoise_signal, np.mean(noise_signal[i - time_horizon : i])
            )
        return denoise_signal

    def simple_plot(
        self, x, y, x_label="x", y_label="y", plot_label="", title="", scatter=False
    ):
        if scatter:
            plt.scatter(x, y, label=plot_label, s=1)
        else:
            plt.plot(x, y, label=plot_label)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.grid(True)
        plt.legend()
        plt.show()

    def plot_generation_decorator(func):
        def wrapper(*args, **kwargs):
            print("In progress: generating the plot...")
            result = func(*args, **kwargs)
            print("Plot generated successfully.")
            return result

        return wrapper

    @plot_generation_decorator
    def mse_horizon_plot(self, signal, max_time_horizon, variance):
        mse, horizon = np.array([]), np.array([])
        noise_signal = self.generate_noise_signal(signal, self.generate_noise(variance))

        for i in range(1, max_time_horizon + 1):
            denoise_signal = self.denoise_filter(noise_signal, i)
            mse = np.append(mse, np.nanmean((signal - denoise_signal) ** 2))
            horizon = np.append(horizon, i)

        self.simple_plot(
            horizon,
            mse,
            "time horizon",
            "MSE",
            "MSE(time horizon)",
            "Mean Squared Error (MSE) dependent on time horizon",
            scatter=True,
        )

    @plot_generation_decorator
    def mse_variance_plot(self, signal, time_horizon, max_variance):
        mse, variance = np.array([]), np.array([])

        for i in np.arange(0.01, max_variance + 0.01, 0.01):
            noise_signal = self.generate_noise_signal(signal, self.generate_noise(i))
            denoise_signal = self.denoise_filter(noise_signal, time_horizon)
            mse = np.append(mse, np.nanmean((signal - denoise_signal) ** 2))
            variance = np.append(variance, i)

        self.simple_plot(
            variance,
            mse,
            "variance",
            "MSE",
            "MSE(variance)",
            "Mean Squared Error (MSE) dependent on variance",
            scatter=True,
        )

    @plot_generation_decorator
    def horizon_variance_plot(self, signal, max_time_horizon, max_variance):
        horizon, variance = np.array([]), np.array([])

        for i in np.arange(0.01, max_variance + 0.01, 0.01):
            noise_signal = self.generate_noise_signal(signal, self.generate_noise(i))
            mse = np.array([])
            for j in range(1, max_time_horizon + 1):
                denoise_signal = self.denoise_filter(noise_signal, j)
                mse = np.append(mse, np.nanmean((signal - denoise_signal) ** 2))
                optimal_horizon = np.where(np.min(mse) == mse)[0][0]
            horizon = np.append(horizon, optimal_horizon)
            variance = np.append(variance, i)

        self.simple_plot(
            variance,
            horizon,
            "variance",
            "horizon",
            "Horizon(variance)",
            "The Optimal Denoising Time Horizon",
            scatter=True,
        )


signal_generator = SignalGenerator(1000, 4)
sin, x = signal_generator.generate_sin()
signal_generator.mse_horizon_plot(sin, 100, 0.5)
signal_generator.mse_variance_plot(sin, 10, 1.5)
signal_generator.horizon_variance_plot(sin, 100, 1.5)
