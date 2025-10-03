"""Module main.py"""
import datetime
import logging
import os
import sys

import boto3
import numpy as np


def main():
    """
    Entry Point<br>
    -----------<br>

    Example:
        members = [277152, 277157, 277164, 277165, 277169, 277171, 277181, 277186]<br>

    :return:
    """

    logger: logging.Logger = logging.getLogger(__name__)
    logger.info('Starting: %s', datetime.datetime.now().isoformat(timespec='microseconds'))

    # Assets
    src.assets.Assets(s3_parameters=s3_parameters).exc()
    specifications_ = src.data.interface.Interface(s3_parameters=s3_parameters).exc()
    members = np.unique(np.array([c.catchment_id for c in specifications_])).tolist()

    # Evaluating predictions
    src.predictions.interface.Interface(arguments=arguments).exc(specifications_=specifications_)

    # Risks
    src.cartography.interface.Interface(
        service=service, s3_parameters=s3_parameters, connector=connector).exc(members=members)

    # Transfer
    src.transfer.interface.Interface(
      connector=connector, service=service, s3_parameters=s3_parameters).exc()

    # Delete Cache Points
    src.functions.cache.Cache().exc()


if __name__ == '__main__':

    # Paths
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # Logging
    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d\n',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Modules
    import src.assets
    import src.cartography.interface
    import src.data.interface
    import src.elements.service as sr
    import src.elements.s3_parameters as s3p
    import src.functions.cache
    import src.predictions.interface
    import src.preface.interface
    import src.transfer.interface

    connector: boto3.session.Session
    s3_parameters: s3p
    service: sr.Service
    arguments: dict
    connector, s3_parameters, service, arguments = src.preface.interface.Interface().exc()

    main()
