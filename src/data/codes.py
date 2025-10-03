"""Module codes.py"""
import glob
import os
import pathlib

import config


class Codes:
    """
    <b>Notes</b><br>
    ------<br>
    Determines the institutions list.<br>
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()

    def __get_codes(self) -> list[str] | None:
        """

        :return:
        """

        listings = glob.glob(pathname=os.path.join(self.__configurations.data_, '**', '**'))

        codes = []
        for listing in listings:
            state = (pathlib.Path(os.path.join(listing, 'estimates.csv')).exists() &
                     pathlib.Path(os.path.join(listing, 'training.csv')).exists() &
                     pathlib.Path(os.path.join(listing, 'testing.csv')).exists())
            if state:
                codes.append(os.path.basename(listing))


        return codes

    def exc(self) -> list[str] | None:
        """

        :return:
        """

        return self.__get_codes()
