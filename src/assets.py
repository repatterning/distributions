"""Module assets.py"""
import glob
import logging
import os
import sys

import config
import src.elements.s3_parameters as s3p
import src.functions.cache
import src.s3.directives
import src.s3.keys
import src.s3.unload


class Assets:
    """
    Notes<br>
    ------<br>

    An interface to the data/artefacts retrieval class.  <b>Beware, sometimes dask
    will be unnecessary, edit accordingly.</b>
    """

    def __init__(self, s3_parameters: s3p.S3Parameters):
        """

        :param s3_parameters: The overarching S3 (Simple Storage Service) parameters
                              settings of this project, e.g., region code name, buckets, etc.
        """

        self.__s3_parameters: s3p.S3Parameters = s3_parameters

        # Setting up
        self.__configurations = config.Config()
        self.__source_bucket = self.__s3_parameters.internal

        # Directives
        self.__directives = src.s3.directives.Directives()

    def __get_assets(self, origin: str) -> int:
        """

        :param origin:
        :return:
        """

        try:
            return self.__directives.unload(
                source_bucket=self.__source_bucket, origin=origin, target=self.__configurations.data_)
        except RuntimeError as err:
            raise err from err

    def exc(self):
        """

        :return:
        """

        origin = self.__configurations.origin_

        # The artefacts, vis-à-vis modelling.
        state = self.__get_assets(origin=origin)
        logging.info('Assets State: %s', state)

        # Third Eye
        listings = glob.glob(pathname=os.path.join(self.__configurations.data_, '**', '*.*'), recursive=True)
        logging.info(listings)
        if len(listings) == 0:
            src.functions.cache.Cache().exc()
            sys.exit('EMPTY ARTEFACTS DIRECTORIES')
