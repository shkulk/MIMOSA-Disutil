"""
Model equations and constraints:
Utility and global welfare

IN WORK
"""
# 170522: changed disutil function from(1 - (m.damage_costs[t, r] if not value(m.ignore_damages) else 0)) to (m.damage_costs[t, r]), m.L(m.year(t), r), m.emdd)


from typing import Sequence
from model.common import (
    AbstractModel,
    Param,
    Var,
    GeneralConstraint,
    RegionalConstraint,
    GlobalConstraint,
    soft_min,
    value
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
    m.emdd = Param()
    m.ignore_damages = Param()

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
                lambda m, t, r: m.disutil_damage[t, r]
                == calc_utility((m.GDP_gross[t, r] * (m.damage_costs[t, r])), m.L(m.year(t), r), m.emdd),
                "disutil_damage",
            ),


# Net utility optimized
            RegionalConstraint(
                lambda m, t, r: m.utility[t, r]
                == m.utility_consumption[t,r] -  m.disutil_damage[t, r],
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
