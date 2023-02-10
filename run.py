from model.mimosa import MIMOSA

from model.common.config import parseconfig


model1 = MIMOSA(parseconfig.params)

#####################
# without Disutility/ default
#####################

# model1.solve()
# model1.save()
# model1.plot()

#####################
# With Disutility
#####################

# # with Disutility (for multiple values for relative disutility factor)
# parseconfig.params["model"]["welfare module"] = "inequal_aversion_elasmu_disutil"
# for disutility_damage_factor in [0.5, 1.00001, 2]:
#     parseconfig.params["economics"]["disutility_damage_factor"] = disutility_damage_factor
#     model1.save()
#     model1.plot()

# with Disutility (for single relative disutility factor value)
# parseconfig.params["model"]["welfare module"] = "inequal_aversion_elasmu_disutil"
# parseconfig.params["economics"]["disutility_damage_factor"] = 2
# model1 = MIMOSA(parseconfig.params)
model1.solve()
model1.save()
model1.plot()

#####################
# both with and without Disutility
#####################

# single damage factor
# parseconfig.params["economics"]["disutility_damage_factor"] = 2

# for welfare_module in [ "inequal_aversion_elasmu", "inequal_aversion_elasmu_disutil"]:
#     parseconfig.params["model"]["welfare module"] = welfare_module
#     model1.solve()
#     model1.save()
#     model1.plot()


