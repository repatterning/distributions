"""Module seasonal.py"""
import os

import pandas as pd

import config
import src.elements.master as mr
import src.elements.specifications as se
import src.elements.text_attributes as txa
import src.functions.objects
import src.functions.streams


class Data:
    """
    <b>Notes</b><br>
    ------<br>

    Retrieves the seasonal component forecasting estimations<br>
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()
        self.__streams = src.functions.streams.Streams()

    def __get_data(self, uri: str) -> pd.DataFrame:
        """

        :param uri: A uniform resource string
        :return:
        """

        text = txa.TextAttributes(uri=uri, header=0)

        return self.__streams.read(text=text)

    def exc(self, specifications: se.Specifications) -> mr.Master:
        """

        :param specifications: Refer to src/elements/specifications.py
        :return:
        """

        # Reading-in
        endpoint = os.path.join(self.__configurations.data_, str(specifications.catchment_id),
                           str(specifications.ts_id))

        return mr.Master(
            estimates=self.__get_data(uri=os.path.join(endpoint, 'estimates.csv')),
            training=self.__get_data(uri=os.path.join(endpoint, 'training.csv')),
            testing=self.__get_data(uri=os.path.join(endpoint, 'testing.csv')))
