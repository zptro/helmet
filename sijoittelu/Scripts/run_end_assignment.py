import sys
import os
import inro.emme.desktop.app as _app
import inro.modeller as _m
import ruma
import hassmat
import trassmat
import kevass
import parameters

filepath = sys.argv[1]
print "Starting Emme..."
emme_desktop = _app.start_dedicated(
    project=filepath, 
    visible=False, 
    user_initials="HSL"
)
emme_modeller = _m.Modeller(emme_desktop)
print "Emme started."

process = emme_modeller.tool(
    "inro.emme.data.function.function_transaction")
default_path = os.path.dirname(emme_modeller.emmebank.path)
function_file = os.path.join(default_path,"d411_pituusriippuvaiset_HM30.in")
process(function_file)

ruma.calc_road_cost(emme_modeller, 21)
ruma.calc_road_cost(emme_modeller, 22)
ruma.calc_road_cost(emme_modeller, 23)

hassmat.traffic_ass(emme_modeller, 21, parameters.stopping_criteria_fine,
                    "mf1", "mf380", "mf381", "mf370")
hassmat.traffic_ass(emme_modeller, 22, parameters.stopping_criteria_fine,
                    "mf2", "mf382", "mf383", "mf371")
hassmat.traffic_ass(emme_modeller, 23, parameters.stopping_criteria_fine,
                    "mf3", "mf384", "mf385", "mf372")

trassmat.transit_ass(emme_modeller, 21, "mf4", "2")
trassmat.transit_ass(emme_modeller, 22, "mf6", "3")
trassmat.transit_ass(emme_modeller, 23, "mf5", "4")

function_file = os.path.join(default_path,"d411_pituusriippuvaiset_pyora.in")
process(function_file)

kevass.bike_ass(emme_modeller, 19, "ms1", "mf386", "@fvol_pt")