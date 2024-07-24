from controllers.adaptive_control import AdaptiveController
from controllers.multilevel_control import MultilevelController
from utils.plotter import unified_plot, radar_plot
import numpy as np


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Control System Simulation and Analysis"
    )
    subparsers = parser.add_subparsers(dest="controller", help="Controller type")

    adaptive_parser = subparsers.add_parser("adaptive", help="Adaptive Controller")
    adaptive_parser.add_argument(
        "--samples", type=int, default=1000, help="Number of samples"
    )
    adaptive_parser.add_argument("--length", type=int, default=6, help="Signal length")
    adaptive_parser.add_argument(
        "--variance", type=float, default=0.1, help="Noise variance"
    )
    adaptive_parser.add_argument("--a0", type=float, default=1, help="Parameter a0")
    adaptive_parser.add_argument("--a1", type=float, default=1, help="Parameter a1")
    adaptive_parser.add_argument("--a2", type=float, default=1, help="Parameter a2")
    adaptive_parser.add_argument(
        "--forgetting_factor", type=float, default=1, help="Forgetting factor"
    )

    multilevel_parser = subparsers.add_parser(
        "multilevel", help="Multilevel Controller"
    )
    multilevel_parser.add_argument(
        "--samples", type=int, default=1000, help="Number of samples"
    )
    multilevel_parser.add_argument(
        "--length", type=int, default=6, help="Signal length"
    )
    multilevel_parser.add_argument(
        "--variance", type=float, default=0.1, help="Noise variance"
    )
    multilevel_parser.add_argument("--a1", type=float, default=0.5, help="Parameter a1")
    multilevel_parser.add_argument("--b1", type=float, default=1, help="Parameter b1")
    multilevel_parser.add_argument(
        "--a2", type=float, default=0.25, help="Parameter a2"
    )
    multilevel_parser.add_argument("--b2", type=float, default=1, help="Parameter b2")

    args = parser.parse_args()

    if args.controller == "adaptive":
        controller = AdaptiveController(args.samples, args.length)
        u_signal, v_signal, y_signal, model_parameters, _, _ = controller.simulate(
            args.variance, args.a0, args.a1, args.a2
        )
        estimated_param, param_hist = controller.identify(
            u_signal, y_signal, args.forgetting_factor
        )
        print(f"True Parameters: a0: {args.a0}, a1: {args.a1}, a2: {args.a2}")
        print(
            f"Estimated Parameters: a0: {estimated_param[0][0]}, a1: {estimated_param[1][0]}, a2: {estimated_param[2][0]}"
        )
        labels = ["$a_0$", "$a_1$", "$a_2$"]
        unified_plot(
            range(len(y_signal)), param_hist, labels, title="Parameter Estimation"
        )

    elif args.controller == "multilevel":
        controller = MultilevelController(args.samples, args.length)
        u_signal, v_signal, y_signal, model_parameters, connection_matrix = (
            controller.simulate(args.variance, args.a1, args.b1, args.a2, args.b2)
        )
        estimated_param = controller.identify(u_signal, y_signal, connection_matrix)
        print(f"True Parameters: {model_parameters.flatten()}")
        print(f"Estimated Parameters: {np.concatenate(estimated_param)}")
        true_values = model_parameters.flatten().tolist()
        estimated_values = np.concatenate(estimated_param).tolist()
        labels = ["$a_1$", "$b_1$", "$a_2$", "$b_2$"]
        radar_plot(true_values, estimated_values, labels, title="Parameter Estimation")


if __name__ == "__main__":
    main()
