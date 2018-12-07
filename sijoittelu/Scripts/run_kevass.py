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
function_file = os.path.join(default_path,"d411_pituusriippuvaiset_pyora.in")
process(function_file)

kevass.bike_ass(emme_modeller, 19, "mf07", "mf386", "@fvol_aht")
kevass.bike_ass(emme_modeller, 19, "mf09", "mf386", "@fvol_pt")
kevass.bike_ass(emme_modeller, 19, "mf08", "mf386", "@fvol_iht")