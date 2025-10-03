"""Module cartography/risks.py"""
import json

import boto3
import dask
import geopandas
import pandas as pd

import src.elements.s3_parameters as s3p
import src.s3.keys
import src.s3.unload


class Risks:
    """
    Data
    """

    def __init__(self, connector: boto3.session.Session, s3_parameters: s3p.S3Parameters, key_name: str):
        """

        :param connector: An instance of boto3.session.Session
        :param s3_parameters: The overarching S3 parameters settings of this
                              project, e.g., region code name, buckets, etc.<br>
        :param key_name: The key name of a bucket data file
        """


        self.__s3_parameters = s3_parameters

        # Instances
        self.__s3_client: boto3.session.Session.client = connector.client(service_name='s3')
        self.__unload = src.s3.unload.Unload(s3_client=self.__s3_client)

        # Data
        self.__data = self.__get_data(key_name=key_name)

    def __get_data(self, key_name: str) -> dict:
        """

        :param key_name:
        :return:
        """

        buffer = self.__unload.exc(bucket_name=self.__s3_parameters.external, key_name=key_name)

        try:
            data = json.loads(buffer)
        except json.JSONDecodeError as err:
            raise err from err

        return data

    @dask.delayed
    def __get_part(self, index: int) -> pd.DataFrame:
        """

        :param index:
        :return:
        """

        node:dict = self.__data[index]
        frame = pd.DataFrame.from_records(data=node['data'], index=node['index'], columns=node['columns'])
        frame['catchment_id'] = node['catchment_id']
        frame['catchment_name'] = node['catchment_name']
        frame['ending_str'] = pd.to_datetime(frame['ending'], unit='ms').dt.strftime("%Y-%m-%d %H:%M:%S")

        return frame

    def exc(self) -> geopandas.GeoDataFrame:
        """

        :return:
        """

        computations = []
        for i in range(len(self.__data)):
            frame = self.__get_part(index=i)
            computations.append(frame)
        structures = dask.compute(computations, scheduler='threads')[0]

        values = pd.concat(structures, axis=0, ignore_index=True)
        c_4326 = geopandas.GeoDataFrame(values, geometry=geopandas.points_from_xy(values.longitude, values.latitude))
        c_4326.crs = 'epsg:4326'

        return c_4326
