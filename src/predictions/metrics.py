"""Module metrics.py"""
import json
import os

import numpy as np
import pandas as pd

import config
import src.elements.specifications as se
import src.elements.structures as st
import src.functions.objects


class Metrics:
    """
    Metrics
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()
        self.__path = os.path.join(self.__configurations.points_, 'errors')

        self.__objects = src.functions.objects.Objects()

    @staticmethod
    def __root_mse(data: pd.DataFrame) -> pd.DataFrame:
        """
        This function calculates
            square root (mean ( a set of square errors ) )
        per set of square errors.

        :param data: A frame of measures, estimates, and errors
        :return:
        """

        square_error: np.ndarray = np.power(data['error'].to_numpy(), 2)
        mse: np.ndarray = np.expand_dims(
            np.sum(square_error, axis=0)/square_error.shape[0], axis=0)

        frame = pd.DataFrame(data=np.sqrt(mse),
                             columns=['errors'], index=['r_mse'])

        return frame

    @staticmethod
    def __pe(data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates the quantile distribution of percentage errors

        :param data: A frame of measures, estimates, and errors
        :return:
        """

        er: np.ndarray = data['p_error'].to_numpy()
        tiles: np.ndarray = np.percentile(a=er, q=[10, 25, 50, 75, 90], axis=0)
        frame = pd.DataFrame(data=tiles, columns=['errors'],
                             index=['l_whisker', 'l_quarter', 'median', 'u_quarter', 'u_whisker'])

        return frame

    def __get_metrics(self, data: pd.DataFrame) -> dict:
        """

        :param data: A frame of measures, estimates, and errors
        :return:
        """

        frame = pd.concat((self.__root_mse(data=data), self.__pe(data=data)),
                          axis=0, ignore_index=False)
        string = frame.to_json(orient='split')

        return json.loads(string)

    def exc(self, structures: st.Structures, specifications: se.Specifications) -> str:
        """

        :param structures: An object of data frames vis-à-vis training, testing, and future predictions
        :param specifications: A gauge's attributes
        :return:
        """

        nodes = {
            'training': self.__get_metrics(data=structures.training),
            'testing': self.__get_metrics(data=structures.testing)}
        nodes.update(specifications._asdict())

        message = self.__objects.write(
            nodes=nodes, path=os.path.join(self.__path, f'{specifications.ts_id}.json'))

        return message
