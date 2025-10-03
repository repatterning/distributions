"""Module interface.py"""
import logging
import os
import pandas as pd

import src.data.codes
import src.data.reference
import src.data.menu
import src.elements.specifications as se
import src.elements.s3_parameters as s3p
import src.data.specifications


class Interface:
    """
    Interface
    """

    def __init__(self, s3_parameters: s3p.S3Parameters):
        """

        :param s3_parameters: The overarching S3 (Simple Storage Service) parameters
                              settings of this project, e.g., region code name, buckets, etc.
        """

        self.__s3_parameters: s3p.S3Parameters = s3_parameters

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d\n',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def exc(self) -> list[se.Specifications]:
        """

        :return:
        """

        _codes: list[str] = src.data.codes.Codes().exc()
        codes = [int(os.path.split(code)[-1]) for code in _codes]
        self.__logger.info(codes)

        reference: pd.DataFrame = src.data.reference.Reference(
            s3_parameters=self.__s3_parameters).exc(codes=codes)
        self.__logger.info(reference)

        src.data.menu.Menu().exc(reference=reference)

        specifications_: list[se.Specifications] = src.data.specifications.Specifications().exc(
            reference=reference)

        return specifications_
