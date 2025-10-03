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
        self.data_ = os.path.join(os.getcwd(), 'data')
        self.warehouse = os.path.join(os.getcwd(), 'warehouse')

        self.latest_ = os.path.join(self.warehouse, 'latest')
        self.points_ = os.path.join(self.latest_, 'points')
        self.menu_ = os.path.join(self.latest_, 'menu')
        self.maps_ = os.path.join(self.latest_, 'maps')

        # The model assets section
        self.origin_ = 'assets/latest'

        # Keys, etc
        self.s3_parameters_key = 's3_parameters.yaml'
        self.argument_key = 'artefacts/architecture/latest/arguments.json'
        self.metadata_ = 'events/external'

        # Prefix
        self.prefix = 'warehouse' + '/' + 'latest'
