""" A module containing an abstract strategy class for analysis methods. """

from abc import ABC, abstractmethod
from pathlib import Path

from experimental_env.experiment.result_description import ResultDescription


class AnalysisStrategy(ABC):
    """
    An abstract strategy class that contains methods for analysis and comparison, as well as a method for establishing a directory
    """

    def __init__(self):
        self._out_dir = "/"

    def set_path(self, path: Path):
        """
        Set the directory where the results of the analysis or comparison will be saved

        :param path: The path to the directory
        """

        self._out_dir = path

    @abstractmethod
    def save_analysis(self):
        """
        Save the results of the analysis or comparison to the installed directory
        """

        raise NotImplementedError

    @abstractmethod
    def analyze_method(self, result: ResultDescription, method: str):
        """
        Analyze the method

        :param result: The result of the method on the second stage of the experiment, which was obtained using a parser.
        :param method: The name of the method that we are analyzing
        """

        raise NotImplementedError

    @abstractmethod
    def compare_methods(
        self,
        result_1: ResultDescription,
        result_2: ResultDescription,
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

        raise NotImplementedError
