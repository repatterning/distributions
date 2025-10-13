"""Module cartography/interface.py"""

import boto3
import geopandas
import pandas as pd

import src.cartography.data
import src.cartography.illustrate
import src.cartography.maps
import src.cartography.reference
import src.cartography.risks
import src.elements.s3_parameters as s3p
import src.s3.keys


class Interface:
    """
    An interface to the risks programs
    """

    def __init__(self, connector: boto3.session.Session, s3_parameters: s3p.S3Parameters):
        """

        :param connector: An instance of boto3.session.Session
        :param s3_parameters: The overarching S3 parameters settings of this
                              project, e.g., region code name, buckets, etc.<br>
        """

        self.__connector = connector
        self.__s3_parameters = s3_parameters

        # Instances
        self.__maps = src.cartography.maps.Maps(connector=self.__connector, s3_parameters=self.__s3_parameters)

    def exc(self, assets: pd.DataFrame):
        """

        :param assets:
        :return:
        """

        # Maps
        coarse = self.__maps.exc(key_name='cartography/coarse.geojson')
        care = self.__maps.exc(key_name='cartography/care_and_coarse_catchments.geojson')
        reference = src.cartography.reference.Reference(s3_parameters=self.__s3_parameters).exc()

        # Building
        data: geopandas.GeoDataFrame = src.cartography.data.Data(care=care, reference=reference).exc()

        # Draw
        src.cartography.illustrate.Illustrate(
            data=data, coarse=coarse, assets=assets).exc(_name='assets')
