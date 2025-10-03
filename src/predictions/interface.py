"""Module src.predictions.interface.py"""
import logging
import os

import dask

import config
import src.elements.master as mr
import src.elements.specifications as se
import src.elements.structures as st
import src.functions.directories
import src.predictions.data
import src.predictions.errors
import src.predictions.metrics
import src.predictions.persist
import src.predictions.structures


class Interface:
    """
    Interface
    """

    def __init__(self, arguments: dict):
        """

        :param arguments:
        """

        self.__arguments = arguments

        # Configurations
        self.__configurations = config.Config()

    def __directories(self):
        """

        :return:
        """

        directories = src.functions.directories.Directories()

        for section in ['predictions', 'errors']:
            path = os.path.join(self.__configurations.points_, section)
            directories.create(path)

    @dask.delayed
    def __get_structures(self, master: mr.Master) -> st.Structures:
        """

        :param master:
        :return:
        """

        return src.predictions.structures.Structures(
            master=master, arguments=self.__arguments).exc()


    def exc(self, specifications_: list[se.Specifications]):
        """

        :param specifications_:
        :return:
        """

        self.__directories()

        __get_data = dask.delayed(src.predictions.data.Data().exc)
        __get_errors = dask.delayed(src.predictions.errors.Errors().exc)
        __persist = dask.delayed(src.predictions.persist.Persist().exc)
        __get_metrics = dask.delayed(src.predictions.metrics.Metrics().exc)

        computations = []
        for specifications in specifications_:

            master = __get_data(specifications=specifications)
            structures = self.__get_structures(master=master)
            structures = __get_errors(structures=structures)
            _measures = __persist(structures=structures, specifications=specifications)
            _metrics = __get_metrics(structures=structures, specifications=specifications)
            computations.append([_measures, _metrics])

        messages = dask.compute(computations, scheduler='threads')[0]
        logging.info(messages)
