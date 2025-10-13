"""Module cartography/interface.py"""
import pathlib

import boto3
import geopandas

import src.cartography.data
import src.cartography.maps
import src.cartography.risks
import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.s3.keys
import src.cartography.illustrate
import src.cartography.reference


class Interface:
    """
    An interface to the risks programs
    """

    def __init__(self, connector: boto3.session.Session, service: sr.Service, s3_parameters: s3p.S3Parameters):
        """

        :param connector: An instance of boto3.session.Session
        :param service: A suite of services for interacting with Amazon Web Services.
        :param s3_parameters: The overarching S3 parameters settings of this
                              project, e.g., region code name, buckets, etc.<br>
        """

        self.__connector = connector
        self.__service = service
        self.__s3_parameters = s3_parameters

        # Instances
        self.__maps = src.cartography.maps.Maps(connector=self.__connector, s3_parameters=self.__s3_parameters)

    def exc(self, members: list[int]):
        """

        :param members:
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
            data=data, coarse=coarse, members=members).exc(_name='assets')
