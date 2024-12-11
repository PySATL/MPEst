""" A module that provides a class for performing the third stage of the experiment """
from pathlib import Path

from tqdm import tqdm

from experimental_env.analysis.analyze_strategies.analysis_strategy import (
    AnalysisStrategy,
)
from experimental_env.experiment.result_description import ResultDescription

ParserOutput = dict[str, list[ResultDescription]]


class Analysis:
    """
    A class that provides a method for analyzing a method or for comparing two methods
    """

    def __init__(self, path: Path, actions: list[AnalysisStrategy]):
        self._out_dir = path
        self._actions = actions

    def analyze(self, results: ParserOutput, method: str):
        """
        A function for analyzing the method

        :param results: The result of the method on the second stage of the experiment, which was obtained using a parser.
        :param method: Name of analyzed method
        """
        method_dir: Path = self._out_dir.joinpath(method)
        if not method_dir.exists():
            method_dir.mkdir()

        for mixture_name, exp_descriptions in results.items():
            mixture_dir: Path = method_dir.joinpath(mixture_name)
            if not mixture_dir.exists():
                mixture_dir.mkdir()

            with tqdm(total=len(exp_descriptions)) as pbar:
                for exp_descr in exp_descriptions:
                    pbar.update()
                    exp_dir = mixture_dir.joinpath(f"experiment_{exp_descr.exp_num}")
                    if not exp_dir.exists():
                        exp_dir.mkdir()

                    for action in self._actions:
                        action.set_path(exp_dir)
                        action.analyze_method(exp_descr, method)

    def compare(
        self,
        results_1: ParserOutput,
        results_2: ParserOutput,
        method_1: str,
        method_2: str,
    ):
        """
        A function for comparing the methods

        :param results_1: The result of the first method on the second stage of the experiment, which was obtained using a parser.
        :param results_1: The result of the second method on the second stage of the experiment, which was obtained using a parser.
        :param method_1: Name of the first method
        :param method_1: Name of the second method
        """
        method_dir = self._out_dir.joinpath(f"{method_1} + {method_2}")
        if not method_dir.exists():
            method_dir.mkdir()

        for mixture_name in results_1.keys():
            mixture_dir = method_dir.joinpath(mixture_name)
            if not mixture_dir.exists():
                mixture_dir.mkdir()

            with tqdm(total=len(results_1[mixture_name])) as pbar:
                for res in zip(results_1[mixture_name], results_2[mixture_name]):
                    pbar.update()
                    exp_dir = mixture_dir.joinpath(f"experiment_{res[0].exp_num}")
                    if not exp_dir.exists():
                        exp_dir.mkdir()

                    for action in self._actions:
                        action.set_path(exp_dir)
                        action.compare_methods(res[0], res[1], method_1, method_2)
