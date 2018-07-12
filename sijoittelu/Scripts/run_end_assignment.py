import sys
import inro.emme.desktop.app as _app
import inro.modeller as _m
import hassmat
import trassmat
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

hassmat.traffic_ass(emme_modeller, 21, parameters.stopping_criteria_fine,
                    "mf1", "mf380", "mf381", "mf370")
hassmat.traffic_ass(emme_modeller, 22, parameters.stopping_criteria_fine,
                    "mf2", "mf382", "mf383", "mf371")
hassmat.traffic_ass(emme_modeller, 23, parameters.stopping_criteria_fine,
                    "mf3", "mf384", "mf385", "mf372")

trassmat.transit_ass(emme_modeller, 21, "mf4", "2")
trassmat.transit_ass(emme_modeller, 22, "mf6", "3")
trassmat.transit_ass(emme_modeller, 23, "mf5", "4")