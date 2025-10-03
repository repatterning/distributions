"""Module src.elements.parts.py"""
import typing

import pandas as pd


class Structures(typing.NamedTuple):
    """
    The data type class ⇾ Structures<br><br>

    Attributes<br>
    ----------<br>
    training<br>
    testing<br>
    futures<br>
    """

    training: pd.DataFrame
    testing: pd.DataFrame
    futures: pd.DataFrame
