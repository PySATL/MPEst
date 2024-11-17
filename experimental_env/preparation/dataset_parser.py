import csv
import os
from pathlib import Path

from numpy import genfromtxt
import yaml

from experimental_env.preparation.dataset_description import DatasetDescrciption
from mpest import Distribution, MixtureDistribution
from mpest.models import ALL_MODELS


class SamplesDatasetParser:
    def parse(self, path: Path) -> dict:
        output = {}
        # Open each mixture dir
        for mixture_name in os.listdir(path):
            mixture_name_dir: Path = path.joinpath(mixture_name)
            mixture_name_dict = {}

            # Open each experiment dir
            for exp in os.listdir(mixture_name_dir):
                experiment_dir: Path = mixture_name_dir.joinpath(exp)
                samples_p: Path = experiment_dir.joinpath("samples.csv")
                config_p: Path = experiment_dir.joinpath("config.yaml")

                # Get samples
                samples = genfromtxt(samples_p, delimiter=',')

                # Get mixture
                with open(config_p, "r") as config_file:
                    config = yaml.safe_load(config_file)
                    samples_size = config["samples_size"]
                    priors = [d["prior"] for d in config["distributions"].values()]
                    dists = [
                        Distribution.from_params(ALL_MODELS[d_name], d_item["params"])
                        for d_name, d_item in config["distributions"].items()
                    ]

                    base_mixture = MixtureDistribution.from_distributions(dists, priors)

                mixture_name_dict[exp] = DatasetDescrciption(
                    samples_size, samples, base_mixture
                )

            output[mixture_name] = mixture_name_dict
        return output