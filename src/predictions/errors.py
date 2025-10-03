"""Module errors.py"""

import numpy as np
import pandas as pd

import src.elements.structures as st


class Errors:
    """
    Errors
    """

    def __init__(self):
        pass

    @staticmethod
    def __get_errors(data: pd.DataFrame) -> pd.DataFrame:
        """

        :param data: A training or testing data set.
        :return:
        """

        # The error with respect to the median, for overarching error calculations
        data.loc[:, 'error'] = data['median'] - data['observation']

        # Calculating error percentages
        estimates = data[['median', 'lower_w', 'upper_w', 'lower_q', 'upper_q']].to_numpy()
        raw = estimates - data['observation'].to_numpy()[:,None]
        percentages = 100*np.true_divide(raw, data['observation'].to_numpy()[:,None])
        data.loc[:, ['p_error', 'p_e_lower_w', 'p_e_upper_w', 'p_e_lower_q', 'p_e_upper_q']] = percentages

        return data

    def exc(self, structures: st.Structures):
        """

        :param structures: Refer to src/elements/structures.py
        :return:
        """

        structures = structures._replace(
            training=self.__get_errors(data=structures.training),
            testing=self.__get_errors(data=structures.testing))

        return structures
