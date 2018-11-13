import sys
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

kevass.bike_ass(emme_modeller, 19, "ms1", "mf386", "@fvol_pt")