@REM *** copy_input_data_HM30.bat
@REM TE 9.8.2017
@REM
@ECHO kopioidaan HELMET 3.0 -ennusteen lahtotietoja
@rem TE 5.4.2017 (aluejako ja kulkutavat M2016)
@rem TE 18.7.2017 (tiedostojen nimiin sij16 tai gr)
@rem TE 5.9.2017  (joidenkin tiedostojen nimiin gr:n asemesta sij16)
@REM WSP/ARa 1.11.2017 (HM30: joidenkin tiedostojen nimiin sij16:n asemesta HM30)
@rem
@IF '%1' EQU '' GOTO VIRHE
@rem
REM ****************************************************************
REM ASETA SEURAAVAT POLKUMAARITYKSET PBL 23.5.2011, TE 5.4.2017
REM HUOM! Rivien lopussa ei saa olla blankkoja!
REM
set    ENNUSTEFOLDER=C:\emme\HELMET_31\ennuste
set SIJOITTELUFOLDER=C:\emme\HELMET_31\sijoittelu
REM ****************************************************************
@rem 
@rem kutsuparametrit:
@rem    1. syottotiedostojen nimessa oleva skenaarion tunnus (esim. 2035_TAV) (max 13 merkkia)
@rem    2. kansio, josta ennustepankin syottotiedostoja kopioidaan
@rem       (.\ = edella maaritelty ENNUSTEFOLDER, .\ALI = edella mainitun alikansio ALI
@rem       Jos muualla, annettava koko polku, esim. C:\helmet_21\ennuste\database\ennustepankkixxxx)
@rem    3. kansio, josta sijoittelupankin syottotiedostoja kopioidaan
@rem       (.\ = edella maaritelty SIJOITTELUFOLDER, muuten syntaksi kuten 2. parametrilla)
@rem
cd  "%ENNUSTEFOLDER%\database"
@rem
rem poistetaan vanhat versiot
del  d311_autonomistus_enn_HM30.in
del  d311_ha_kmkust_HM20.in
del  d311_jlkust_14_kuntaa_sij16.in
del  d311_oppilaspaikat_sij16.in
del  d311_pysakointi_kust_sij16.in
del  d311_tyopaikat_HM30.in
del  d311_ulkoiset_kasvukerroin_gr.in
del  d311_vaesto_14_kuntaa_sij16.in
del  d311_vaesto_ymparyskunnat_sij19.in
@rem
rem kopioidaan vaihtoehdon %1 lahtotiedot
copy %2\d311_autonomistus_enn_%1_HM30.in       d311_autonomistus_enn_HM30.in
copy %2\d311_ha_kmkust_%1_HM20.in              d311_ha_kmkust_HM20.in
copy %2\d311_jlkust_14_kuntaa_%1_sij16.in      d311_jlkust_14_kuntaa_sij16.in
copy %2\d311_oppilaspaikat_%1_sij16.in         d311_oppilaspaikat_sij16.in
copy %2\d311_pysakointi_kust_%1_sij16.in       d311_pysakointi_kust_sij16.in
copy %2\d311_tyopaikat_%1_HM30.in              d311_tyopaikat_HM30.in
copy %2\d311_ulkoiset_kasvukerroin_%1_gr.in    d311_ulkoiset_kasvukerroin_gr.in
copy %2\d311_vaesto_14_kuntaa_%1_sij16.in      d311_vaesto_14_kuntaa_sij16.in
copy %2\d311_vaesto_ymparyskunnat_%1_sij19.in  d311_vaesto_ymparyskunnat_sij19.in
@rem
cd  "%SIJOITTELUFOLDER%\database"
@rem
rem poistetaan vanhat versiot
del  d311_jakoluvut_enn13_sij19.in
del  d311_matktermkys_sij19.in
del  d311_tama_ennustevektorit_sij19.in
@rem
rem kopioidaan vaihtoehdon %1 lahtotiedot
copy %3\d311_jakoluvut_enn13_sij19_%1.in       d311_jakoluvut_enn13_sij19.in
copy %3\d311_matktermkys_%1_sij19.in           d311_matktermkys_sij19.in
copy %3\d311_tama_ennustevektorit_%1_sij19.in  d311_tama_ennustevektorit_sij19.in
@rem
cd  ..\..\
cd
GOTO LOPPU 
@REM
:VIRHE
ECHO Anna parametrit (1. pakollinen, 2. ja 3. vain, jos tiedostot eivat ole nykyisessa kansiossa)
ECHO 1. skenaarion tunnus, joka on ennustekansion tiedostojen nimissa (esimerkiksi 2020niukka)
ECHO 2. sen kansion nimi, josta tiedostot kopioidaan ennustepankkiin    (esim.  .\2020niukka\, oletus nykyinen)
ECHO 3. sen kansion nimi, josta tiedostot kopioidaan sijoittelupankkiin (esim.  .\sijopankki2020\, oletus nykyinen)
:LOPPU