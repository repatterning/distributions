"""Module interface.py"""
import sys
import typing

import boto3

import config
import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.functions.cache
import src.functions.service
import src.preface.setup
import src.s3.configurations
import src.s3.s3_parameters


class Interface:
    """
    Interface
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()

    def __get_arguments(self, connector: boto3.session.Session) -> dict:
        """

        :param connector:
            <a href='https://boto3.amazonaws.com/v1/documentation/api/latest/guide/session.html#custom-session'>
            A boto3 custom session.</a><br>
        :return:
        """

        key_name = self.__configurations.argument_key

        return src.s3.configurations.Configurations(connector=connector).objects(key_name=key_name)

    def exc(self) -> typing.Tuple[boto3.session.Session, s3p.S3Parameters, sr.Service, dict]:
        """

        :return:
        """

        connector = boto3.session.Session()
        arguments: dict = self.__get_arguments(connector=connector)

        s3_parameters: s3p.S3Parameters = src.s3.s3_parameters.S3Parameters(
            connector=connector).exc()
        service: sr.Service = src.functions.service.Service(
            connector=connector, region_name=s3_parameters.region_name).exc()

        setup = src.preface.setup.Setup().exc()
        if setup:
            return connector, s3_parameters, service, arguments

        src.functions.cache.Cache().exc()
        sys.exit('Unable to set up local environments.')
