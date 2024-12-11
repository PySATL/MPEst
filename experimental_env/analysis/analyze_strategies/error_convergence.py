""" A module providing a class for saving the convergence graph of the error function. """

from matplotlib import pyplot as plt

from experimental_env.analysis.analyze_strategies.analysis_strategy import (
    AnalysisStrategy,
)
from experimental_env.analysis.metrics import AMetric
from experimental_env.experiment.result_description import ResultDescription


class ErrorConvergence(AnalysisStrategy):
    """
    A class that saves graphs with errors at each step.
    The constructor accepts an error function that satisfies the AMetric interface.
    """

    def __init__(self, metric: AMetric):
        super().__init__()
        self._metric = metric

    def save_analysis(self):
        plt.legend()
        plt.yscale("log")
        plt.savefig(self._out_dir / "error_convergence_plot.png")
        plt.close()

    def analyze_method(self, result: ResultDescription, method: str):
        steps = result.steps
        base_mixture = result.base_mixture
        mixtures = [step.result_mixture for step in steps]

        metric_errors = [self._metric.error(base_mixture, mxt) for mxt in mixtures]
        plt.title(self._metric.name)
        plt.xlabel("Step")
        plt.ylabel("Error")

        plt.plot(
            metric_errors, label=f"Average: {sum(metric_errors) / len(metric_errors)}"
        )

        self.save_analysis()

    def compare_methods(
        self,
        result_1: ResultDescription,
        result_2: ResultDescription,
        method_1: str,
        method_2: str,
    ):
        steps_1, steps_2 = result_1.steps, result_2.steps
        base_mixture = result_1.base_mixture

        mixtures_1 = [step.result_mixture for step in steps_1]
        mixtures_2 = [step.result_mixture for step in steps_2]

        metric_errors_1 = [self._metric.error(base_mixture, mxt) for mxt in mixtures_1]
        metric_errors_2 = [self._metric.error(base_mixture, mxt) for mxt in mixtures_2]

        plt.title(self._metric.name)
        plt.xlabel("Step")
        plt.ylabel("Error")

        plt.plot(
            metric_errors_1,
            label=f"{method_1}. Average: {sum(metric_errors_1) / len(metric_errors_1)}",
        )
        plt.plot(
            metric_errors_2,
            label=f"{method_2}. Average: {sum(metric_errors_2) / len(metric_errors_2)}",
        )

        self.save_analysis()
