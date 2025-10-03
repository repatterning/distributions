"""Module setup.py"""
import config
import src.functions.directories


class Setup:
    """
    Description
    -----------

    Sets up local environments
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()
        self.__directories = src.functions.directories.Directories()

    def __local(self) -> bool:
        """

        :return:
        """

        self.__directories.cleanup(path=self.__configurations.warehouse)

        return self.__directories.create(self.__configurations.maps_)

    def exc(self) -> bool:
        """

        :return:
        """

        return self.__local()
