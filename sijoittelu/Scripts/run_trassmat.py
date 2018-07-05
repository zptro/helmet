import inro.emme.desktop.app as _app
import inro.modeller as _m
import trassmat

emme_desktop = _app.start_dedicated(
    project="C:\Helmet\HELMET_KEHI_31\sijoittelu\sijoittelu.emp", 
    visible=False, 
    user_initials="HSL"
)
emme_modeller = _m.Modeller(emme_desktop)

trassmat.transit_ass(emme_modeller, 21, "mf4", "2")
trassmat.transit_ass(emme_modeller, 22, "mf6", "3")
trassmat.transit_ass(emme_modeller, 23, "mf5", "4")