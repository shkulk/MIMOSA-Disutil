"""
Model equations and constraints:
Utility and global welfare
"""

from typing import Sequence
from model.common import (
    AbstractModel,
    Param,
    Var,
    GeneralConstraint,
    RegionalConstraint,
    GlobalConstraint,
    soft_min,
)


def get_constraints(m: AbstractModel) -> Sequence[GeneralConstraint]:
    """Utility and welfare equations

    Necessary variables:
        m.utility
        m.welfare

    Returns:
        list of constraints (any of:
           - GlobalConstraint
           - GlobalInitConstraint
           - RegionalConstraint
           - RegionalInitConstraint
        )
    """
    constraints = []

    # Parameters
    m.elasmu = Param()
    m.disutility_damage_factor = Param()
    # m.disutility_switch = Param()

    m.utility_consumption = Var(m.t, m.regions, initialize=0.1)
    m.yearly_welfare = Var(m.t)

    m.utility = Var(m.t, m.regions, initialize=0.1)    
    m.utility_less_mit = Var(m.t, m.regions, initialize=0.1)
    m.disutil_damage = Var(m.t, m.regions, initialize=0.1)


    constraints.extend(
        [
            RegionalConstraint(
                lambda m, t, r: m.utility_consumption[t, r]
                == calc_utility(m.consumption[t, r], m.L(m.year(t), r), m.elasmu),
                "utility_consumption",
            ),

            RegionalConstraint(
                lambda m, t, r: m.utility_less_mit[t, r]
                == calc_utility(((1- m.sr)* m.GDP_less_mit[t,r]), m.L(m.year(t), r), m.elasmu),
                "utility_less_mitigation_costs",
            ),
            RegionalConstraint(
                lambda m, t, r: m.disutil_damage[t, r]
                == m.disutility_damage_factor * (m.utility_less_mit[t,r] - m.utility_consumption[t,r]),
                "disutil_damage",
            ),
# Net utility optimized
            RegionalConstraint(
                lambda m, t, r: m.utility[t, r]
                == m.utility_less_mit[t,r] -  m.disutil_damage[t, r],
                "utility",
            ),



            GlobalConstraint(
                lambda m, t: m.yearly_welfare[t]
                == sum(m.L(m.year(t), r) * m.utility[t, r] for r in m.regions),
                "yearly_welfare",
            ),

        ]
    )

    return constraints


def calc_utility(consumption, population, elasmu):
    return (soft_min(consumption / population) ** (1 - elasmu) - 1) / (1 - elasmu) - 1
