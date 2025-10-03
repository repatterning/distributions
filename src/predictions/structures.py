"""Module structures.py"""
import pandas as pd

import src.elements.master as mr
import src.elements.structures as st


class Structures:
    """
    Builds the training, testing, and futures data structures
    """

    def __init__(self, master: mr.Master, arguments: dict):
        """

        :param master:
        :param arguments:
        """

        self.__master = master
        self.__arguments = arguments

        # Estimates
        estimates = master.estimates
        estimates['date'] = pd.to_datetime(estimates['timestamp'], unit='us')
        estimates.drop(columns='timestamp', inplace=True)
        self.__estimates = estimates.sort_values(by='date', ascending=True, inplace=False)

    def __training(self):
        """

        :return:
        """

        training = self.__master.training
        training['date'] = pd.to_datetime(training['timestamp'], unit='ms')

        data = training[['date']].merge(self.__estimates, how='left', on='date')

        return data

    def __testing(self):
        """

        :return:
        """

        testing = self.__master.testing
        testing['date'] = pd.to_datetime(testing['timestamp'], unit='ms')

        data = testing[['date']].merge(self.__estimates, how='left', on='date')

        return data

    def __futures(self):
        """

        :return:
        """

        return self.__estimates[-self.__arguments.get('ahead'):]

    def exc(self) -> st.Structures:
        """

        :return:
        """

        return st.Structures(
            training=self.__training(), testing=self.__testing(), futures=self.__futures())
