"""Module priorities.py"""
import typing


class Parcel(typing.NamedTuple):
    """
    The data type class ⇾ Priorities<br><br>

    Attributes<br>
    ----------<br>
    <b>catchment_id</b>: int<br>
        The identification code of a catchment area.<br><br>
    <b>catchment_name</b>: str<br>
        The corresponding catchment name.<br><br>
    <b>decimal</b>: float<br>
        A decimal number for colour coding.<br><br>
    <b>warning</b>: bool<br>
        Included in the latest warning?
    """

    catchment_id: int
    catchment_name: str
    decimal: float
    warning: bool
