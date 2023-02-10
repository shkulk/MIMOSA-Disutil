from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass
class UnitValues:
    xvalues: Iterable
    yvalues: Iterable
    unit: str = None


def extrapolate(input_values, years, extra_years, meta_info, stabilising_years=50):
    """
    To extrapolate: take growth rate 2090-2100, linearly bring it down to growth rate of 0 in 2150
    """

    became_negative = False

    # First get final change rate
    change_rate = (input_values[-1] - input_values[-2]) / (years[-1] - years[-2])
    minmax = np.maximum if change_rate > 0 else np.minimum

    t_prev = years[-1]
    val_prev = input_values[-1]

    new_values = []

    for t in extra_years:
        change = minmax(
            0.0, change_rate - change_rate * (t_prev - 2100.0) / stabilising_years
        )
        val = val_prev + change * (t - t_prev)
        # if val < 0:
        #     val = 0.1
        #     became_negative = True

        new_values.append(val)

        val_prev = val
        t_prev = t

    if became_negative:
        print("Extrapolation became negative for", meta_info)
    return np.concatenate([input_values, new_values])
