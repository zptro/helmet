import inro.emme.desktop.app as _app
import inro.modeller as _m
import hassmat

emme_desktop = _app.start_dedicated(
    project="C:\Helmet\HELMET_KEHI_31\sijoittelu\sijoittelu.emp", 
    visible=False, 
    user_initials="HSL"
)
emme_modeller = _m.Modeller(emme_desktop)

hassmat.traffic_ass(emme_modeller, 21, "mf1", "mf380", "mf381", "mf370")