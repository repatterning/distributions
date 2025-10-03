"""config.py"""
import os


class Config:
    """
    Config
    """

    def __init__(self) -> None:
        """
        Constructor<br>
        -----------<br>

        Variables denoting a path - including or excluding a filename - have an underscore suffix; this suffix is
        excluded for names such as warehouse, storage, depository, etc.<br><br>
        """

        # The project's key name
        self.project_key_name = 'HydrographyProject'

        # Directories
        self.warehouse = os.path.join(os.getcwd(), 'warehouse')
        self.distributions_ = os.path.join(self.warehouse, 'distributions')
        self.maps_ = os.path.join(self.distributions_, 'maps')

        # Prefix
        self.prefix = self.distributions_.replace(os.getcwd() + os.sep, '')

        # The model assets section
        self.origin_ = 'assets/latest'

        # Keys, etc
        self.s3_parameters_key = 's3_parameters.yaml'
        self.argument_key = 'artefacts/architecture/latest/arguments.json'
        self.metadata_ = 'distributions/external'
