""" A module that provides a class for saving a graph showing the execution time of each step """

import matplotlib.pyplot as plt

from experimental_env.analysis.analyze_strategies.analysis_strategy import (
    AnalysisStrategy,
)
from experimental_env.experiment.result_description import ResultDescription


class TimePlot(AnalysisStrategy):
    """
    A class that saves a time graph at each step.
    """

    def save_analysis(self):
        plt.legend()
        plt.yscale("log")
        plt.savefig(self._out_dir / "time_plot.png")
        plt.close()

    def analyze_method(self, result: ResultDescription, method: str):
        steps = result.steps
        time = [step.time for step in steps]
        plt.plot(time, label=f"Total: {sum(time)}s")
        plt.xlabel("Step")
        plt.ylabel("Time [s]")
        self.save_analysis()

    def compare_methods(
        self,
        result_1: ResultDescription,
        result_2: ResultDescription,
        method_1: str,
        method_2: str,
    ):
        steps_1, steps_2 = result_1.steps, result_2.steps
        time_1 = [step.time for step in steps_1]
        time_2 = [step.time for step in steps_2]

        plt.plot(time_1, color="green", label=f"{method_1}. Total time: {sum(time_1)}s")
        plt.plot(time_2, color="red", label=f"{method_2}. Total time: {sum(time_2)}s")
        plt.xlabel("Step")
        plt.ylabel("Time [s]")
        self.save_analysis()
