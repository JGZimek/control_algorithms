import matplotlib.pyplot as plt
import numpy as np


def unified_plot(x, y, labels, title="", plot_type="line", xlabel="X", ylabel="Y"):
    """
    Create a unified plot for line or scatter plots.

    Args:
        x (ndarray): X values for the plot.
        y (list of ndarrays): Y values for the plot.
        labels (list of str): Labels for each line/scatter in the plot.
        title (str): Title of the plot.
        plot_type (str): Type of plot ('line' or 'scatter').
        xlabel (str): Label for the X axis.
        ylabel (str): Label for the Y axis.
    """
    plt.figure()
    if plot_type == "line":
        for data, label in zip(y, labels):
            plt.plot(x, data, label=label)
    elif plot_type == "scatter":
        for data, label in zip(y, labels):
            plt.scatter(x, data, label=label, s=1)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.show()


def radar_plot(true_values, estimated_values, labels, title=""):
    """
    Create a radar plot for comparing true and estimated values.

    Args:
        true_values (list): List of true values.
        estimated_values (list): List of estimated values.
        labels (list of str): Labels for each axis.
        title (str): Title of the plot.
    """
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]
    true_values += true_values[:1]
    estimated_values += estimated_values[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, true_values, color="blue", alpha=0.25)
    ax.plot(angles, true_values, color="blue", linewidth=2, label="True Values")
    ax.fill(angles, estimated_values, color="red", alpha=0.25)
    ax.plot(
        angles, estimated_values, color="red", linewidth=2, label="Estimated Values"
    )

    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    plt.title(title)
    plt.legend(loc="upper right", bbox_to_anchor=(0.1, 0.1))
    plt.show()
