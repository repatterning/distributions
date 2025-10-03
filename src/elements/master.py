"""Module src.elements.master.py"""
import typing

import pandas as pd


class Master(typing.NamedTuple):
    """
    The data type class ⇾ Master<br><br>

    Attributes<br>
    ----------<br>
    estimates<br>
    training<br>
    testing<br>
    """

    estimates: pd.DataFrame
    training: pd.DataFrame
    testing: pd.DataFrame
