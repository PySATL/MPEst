"""Module which describes dataset"""
import copy

from mpest.mixture_distribution import MixtureDistribution
from mpest.types import Samples


class DatasetDescrciption:
    """
    The class that contains the configuration for the dataset.
    """

    def __init__(
        self, samples_size: int, samples: Samples, base_mixture: MixtureDistribution
    ):
        self._samples_size = samples_size
        self._samples = samples
        self._base_mixture = copy.deepcopy(base_mixture)

    @property
    def samples_size(self) -> int:
        """
        Property for sample size
        """
        return self._samples_size

    @property
    def base_mixture(self) -> MixtureDistribution:
        """
        Property for base mixture
        """
        return self._base_mixture

    @property
    def samples(self):
        """
        Property for samples
        """
        return self._samples

    def get_dataset_name(self) -> str:
        """
        Get dataset name
        """
        return "".join(d.model.name for d in self._base_mixture)

    def to_yaml_format(self) -> dict:
        """
        Convert info about mixture to yaml format
        """
        # pylint: disable=duplicate-code

        output = {}
        # Add name
        output["name"] = self.get_dataset_name()
        output["samples_size"] = self.samples_size

        # Get params of distributions
        dists = []
        for d in self._base_mixture:
            dists.append(
                {
                    "type": d.model.name,
                    "params": d.params.tolist(),
                    "prior": float(d.prior_probability),
                }
            )
        output["distributions"] = dists

        return output
