"""Functions for experimental environment"""
import re

from experimental_env.analysis.metrics import Parametric
from mpest import Distribution, MixtureDistribution, Problem
from mpest.models import ALL_MODELS
from mpest.utils import ResultWithLog


def create_mixture_by_key(config: dict, key: str) -> MixtureDistribution:
    """
    A function that simplifies the creation of a mix from a config file.
    """
    # Read even one element as list
    if not isinstance(config[key], list):
        config[key] = [config[key]]

    priors = [d["prior"] for d in config[key]]
    dists = [
        Distribution.from_params(ALL_MODELS[d["type"]], d["params"])
        for d in config[key]
    ]

    return MixtureDistribution.from_distributions(dists, priors)


def choose_best_mle(
    base_mixture: MixtureDistribution, results: list[ResultWithLog]
) -> ResultWithLog:
    """
    The method for choosing the best result in the maximum likelihood method
    """
    best_result = results[0]

    for result in results:
        res_mixture = result.content.content
        if Parametric().error(base_mixture, res_mixture) < Parametric().error(
            base_mixture, best_result.content.content
        ):
            best_result = result

    return best_result


class OrderedProblem(Problem):
    """
    The class needed to solve the problem of disorder in the problem list.
    Indicates the experiment number to which this problem relates.
    """

    def __init__(self, samples, distributions, number: int):
        super().__init__(samples, distributions)
        self._number = number

    @property
    def number(self):
        """
        Property of number.
        """
        return self._number


def sort_human(l: list):
    """
    Function for sorting list in alphanumerical order.
    """
    # pylint: disable = [unnecessary-lambda-assignment]
    convert = lambda text: float(text) if text.isdigit() else text
    alphanum = lambda key: [
        convert(c) for c in re.split(r"([-+]?[0-9]*\.?[0-9]*)", key)
    ]
    return sorted(l, key=alphanum)
