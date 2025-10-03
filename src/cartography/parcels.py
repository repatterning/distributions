"""Module parcels.py"""
import geopandas
import numpy as np
import pandas as pd

import src.elements.parcel as pcl


class Parcels:
    """
    Parcels
    """

    def __init__(self, data: geopandas.GeoDataFrame):
        """

        :param data: The frame of metrics per gauge station.
        """

        self.__data = data

        # Seed
        self.__seed = 5

    def __get_decimals(self, size: int):
        """

        :param size: The number of required random numbers
        :return:
        """

        rng = np.random.default_rng(seed=self.__seed)

        return rng.uniform(low=0.05, high=0.80, size=size)

    def __catchments(self) -> pd.DataFrame:
        """

        :return:
        """

        frame = self.__data[['catchment_id', 'catchment_name']].drop_duplicates()

        # Hence
        frame.sort_values(by='catchment_name', inplace=True)
        frame.reset_index(drop=True, inplace=True)

        return frame

    def exc(self, members: list) -> list[pcl.Parcel]:
        """

        :param members:
        :return:
        """

        catchments = self.__catchments()
        catchments['decimal'] = self.__get_decimals(size=catchments.shape[0])
        catchments['warning'] = catchments['catchment_id'].isin(members).values

        # An iterable for mapping by layer
        values: list[dict] = catchments.to_dict(orient='records')
        parcels = [pcl.Parcel(**value) for value in values]

        return parcels
