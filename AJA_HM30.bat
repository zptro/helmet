REM *** AJA_HM30.BAT  ***
@rem 
@rem ARa 17.6.2010, TE 6.6.2013, ARa 2.7.2013 (HM20)
@rem ARA 30.7.2013 (Emme 4), TE 19.2.2014
@rem ARA 3.6.2014 (HM21), TE 18.7.2014 (mf07-mf09)
@rem TE 15.1.2015 (.lis --> .txt)
@rem TE 2.6.2015 (yhdistetty HELMETPATH-maarittely foldereihin)
@rem TE 7.4.2017 (aluejako ja kulkutavat M2016)
@rem TE 22.6.2017 (matriisien siirto emmepankkien valilla ilman levylle tulostamista)
@rem ARa 3.11.2017 (HM30)
@rem JWest 2.12.2017 (hankearvdata.py lisatty)
@rem TE 10.1.2018 alkukysynta luetaan ennustepankkiin ja importataan sielta sijoittelupankkiin
@rem TE 18.1.2018 vastusmatriisien deletoinnit ja kopioinnit kommenteiksi, tehdaan makroissa
@rem
@rem 
@rem kutsuparametrit:
@rem    1. kierrosmaara (yleensa 10)
@rem    2. skenaarion tunnus (esim. 2035_TAV) (max 13 merkkia)
@rem 
REM ****************************************************************
REM ASETA SEURAAVAT POLKUMAARITYKSET PBL 23.5.2011, TE 11.7.2014
REM HUOM! Rivien lopussa ei saa olla blankkoja!
REM
set    ENNUSTEFOLDER="C:\Helmet\HELMET_KEHI_31\ennuste"
set SIJOITTELUFOLDER="C:\Helmet\HELMET_KEHI_31\sijoittelu"
REM ****************************************************************
@rem 
path=%EMMEPATH%\\Programs;%PATH%
@IF %1 LSS 2  GOTO VIRHE
@rem
@IF '%1' EQU '' GOTO VIRHE
@rem
@echo syotetty kierrosmaara %1 
@rem
@rem *** ENNUSTEAJON VALMISTELU ***
@rem
REM Siirrytaan hakemistoon, jossa ennustepankki on
C:
cd "%ENNUSTEFOLDER%\Database"
@rem
DEL bat_loki_ka.txt 
ECHO Ennusteajo keskiarvovastuksin alkaa, syotetty kierrosmaara %1, summaustaso EI (= ei aggregoida), tunnus %2 >> bat_loki_ka.txt
ECHO Sijoittelupankki on kansiossa %SIJOITTELUFOLDER%\Database >> bat_loki_ka.txt
ECHO Ennustepankki    on kansiossa %ENNUSTEFOLDER%\Database    >> bat_loki_ka.txt
date /t >> bat_loki_ka.txt
time /t >> bat_loki_ka.txt
@rem
@rem Kaynnistetaan Emme ennustepankissa suoraan makroon, joka tekee kaiken tarvittavan
@rem  (sama kuin ei-keskiarvoistetuilla vastuksilla)
Emme -ng -m cmd-makro_enn_lahto_HM30.mac
@rem
@rem ECHO lahtotiedot luettu ennustepankkiin >> bat_loki_ka.txt
date /t >> bat_loki_ka.txt
time /t >> bat_loki_ka.txt
ECHO ---------- >> bat_loki_ka.txt
@rem
@rem *** SIJOITTELUN VALMISTELU JA 1. SIJOITTELUAJO ***
@rem 
REM Siirrytaan hakemistoon, jossa sijoittelupankki on
C:
cd "%SIJOITTELUFOLDER%\Database"
@rem
@rem kopioidaan alkukysynta ennustepankista
Emme -ng -m import.mac %ENNUSTEFOLDER% mf01 mf06
@rem
@rem Kaynnistetaan Emme sijoittelupankissa suoraan makroon, joka tekee kaiken
@rem  sijoittelun valmistelussa tarvittavan
Emme -ng -m cmd-makro_sij_lahto_HM30.mac
@rem
date /t >> %ENNUSTEFOLDER%\database\bat_loki_ka.txt
time /t >> %ENNUSTEFOLDER%\database\bat_loki_ka.txt
ECHO ---------- >> %ENNUSTEFOLDER%\database\bat_loki_ka.txt
@rem
@rem Tuhotaan hakemistossa mahdollisesti jo olevat tiedostot jakoluvut.EImax ja vastusmatriisit.EIsum
DEL jakoluvut.EImax vastusmatriisit.EIsum
@rem Tuhotaan hakemistossa mahdollisesti jo olevat "vastus*tayd*.txt" -tiedostot
@rem seka ha-, kevyt ja ruuhkamaksu -.txt -tiedostot (ha*vastus.txt)
REM *** DEL ha*vastus.txt vastus*tayd*.txt
@rem
@rem Kaynnistetaan Emme sijoittelupankissa suoraan makroon, joka tekee kaiken tarvittavan
Emme -ng -m cmd-makro_sij_sij16.mac  1  EI  %2
Emme -ng -m valivastus2_sij16.mac   1
@rem
@rem Siirretaan talteen "*.txt"tiedostot, eli vastukset eri muodossa
@rem (jos sijoittelupankin databasessa on hakemisto "vastukset")
REM *** COPY ha*vastus.txt vastukset\ha*vastus.txt_%%X
REM *** COPY "vastus*tayd*.txt" vastukset\vastus*.txt_%%X
@rem
REM Siirrytaan hakemistoon, jossa ennustepankki on
C:
cd "%ENNUSTEFOLDER%\Database"
@rem
ECHO Sijoittelut pohjakysynnalla tehty >> bat_loki_ka.txt
date /t >> bat_loki_ka.txt
time /t >> bat_loki_ka.txt
ECHO ---------- >> bat_loki_ka.txt
@rem
@rem ****************************************************************
REM ****** LUUPPI ALKAA ******
@rem
@rem *** iteraatiokierrokset 2..X (eli X-1 kierrosta)
@rem
@rem Kierrosmaara annetaan parametrina skriptin kaynnistyksen yhteydessa.
@rem Ennen luupin alkua on jo ajettu yksi kierros eli yhteensa X kierrosta
@rem Esimerkiksi jos x=4, niin saadaan (2,1,4), joka tarkoittaa, etta
@rem aloituskierroksen jalkeen ajetaan kierrokset 2, 3 ja 4 eli yhteensa 4.
@rem
FOR /L %%X in (2,1,%1%) do (
@rem 
@rem *** ENNUSTEAJO ***
@rem
@rem Poistetaan vanhat vastusmatriisit ja kopioidaan uudet sijoittelupankista
Emme -ng -m matin.mac  d311_del_vastukset_HM21.in
Emme -ng -m import.mac %SIJOITTELUFOLDER% mf10  mf18
Emme -ng -m import.mac %SIJOITTELUFOLDER% mf28  mf30
Emme -ng -m import.mac %SIJOITTELUFOLDER% mf34  mf34
Emme -ng -m import.mac %SIJOITTELUFOLDER% mf51  mf53
Emme -ng -m import.mac %SIJOITTELUFOLDER% mf398 mf400
@REM
@rem Kaynnistetaan Emme ennustepankissa suoraan makroon, joka tekee kaiken tarvittavan
Emme -ng -m cmd-makro_enn_HM30_ka.mac %%X  %2
@rem
date /t >> bat_loki_ka.txt
time /t >> bat_loki_ka.txt
ECHO ---------- >> bat_loki_ka.txt
@rem
REM *** COPY mf01_06_mf693_695.txt  mf01_06_mf693_695.txt_%%X
@rem
@rem *** SIJOITTELUAJO ***
@rem 
REM Siirrytaan hakemistoon, jossa sijoittelupankki on
C:
cd "%SIJOITTELUFOLDER%\Database"
@rem
@rem Tuhotaan hakemistossa mahdollisesti jo olevat tiedostot jakoluvut.EImax ja vastusmatriisit.EIsum
DEL jakoluvut.EImax vastusmatriisit.EIsum
@rem Tuhotaan hakemistossa mahdollisesti jo olevat "vastus*tayd*.txt" -tiedostot
@rem seka ha-, kevyt ja ruuhkamaksu -.txt -tiedostot (ha*vastus.txt)
REM *** DEL ha*vastus.txt vastus*tayd*.txt
@rem
@rem Poistetaan vanhat ha-matkamatriisit ja kopioidaan uudet ennustepankista
Emme -ng -m matin.mac  d311_del_ajoneuvokysyntaW.in
Emme -ng -m import.mac %ENNUSTEFOLDER% mf01 mf03
@REM
@rem Kaynnistetaan Emme sijoittelupankissa suoraan makroon, joka tekee kaiken tarvittavan
Emme -ng -m cmd-makro_sij_sij16.mac %%X  EI  %2
Emme -ng -m valivastus2_sij16.mac  %%X
@rem
@rem Siirretaan talteen "*.txt"tiedostot, eli vastukset eri muodossa
@rem (jos sijoittelupankin databasessa on hakemisto "vastukset")
REM *** COPY ha*vastus.txt vastukset\ha*vastus.txt_%%X
REM *** COPY "vastus*tayd*.txt" vastukset\vastus*.txt_%%X
@rem
REM Siirrytaan hakemistoon, jossa ennustepankki on
C:
cd "%ENNUSTEFOLDER%\Database"
@rem
ECHO Iteraatiokierros %%X ajettu >> bat_loki_ka.txt
date /t >> bat_loki_ka.txt
time /t >> bat_loki_ka.txt
ECHO ---------- >> bat_loki_ka.txt
)
REM ****** LUUPPI PAATTYY ******
@rem ****************************************************************
@rem
@rem *** Viimeinen iteraatiokierros (hiukan erilainen, 
@rem mm. suuntautumiskorjaus tehdaan vain viimeisella kerralla)
@rem 
@rem *** ENNUSTEAJO ***
@rem
@rem Poistetaan vanhat vastusmatriisit ja kopioidaan uudet sijoittelupankista
Emme -ng -m matin.mac  d311_del_vastukset_HM21.in
Emme -ng -m import.mac %SIJOITTELUFOLDER% mf10  mf18
Emme -ng -m import.mac %SIJOITTELUFOLDER% mf28  mf30
Emme -ng -m import.mac %SIJOITTELUFOLDER% mf34  mf34
Emme -ng -m import.mac %SIJOITTELUFOLDER% mf51  mf53
Emme -ng -m import.mac %SIJOITTELUFOLDER% mf398 mf400
@REM
@rem Kaynnistetaan Emme ennustepankissa suoraan makroon, joka tekee kaiken tarvittavan
Emme -ng -m cmd-makro_enn_vika_HM30_ka.mac  %2
@rem
REM *** COPY mf01_06_mf693_695.txt  mf01_06_mf693_695.txt_99
@rem
ECHO Viimeinen ennustekierros (koodi 99) ajettu >> bat_loki_ka.txt
date /t >> bat_loki_ka.txt
time /t >> bat_loki_ka.txt
ECHO ---------- >> bat_loki_ka.txt
@rem
@rem *** SIJOITTELUAJO ***
@rem 
@rem sijoittelu ennustetulla kysynnalla (mutta samoilla, pituusriippuvaisilla funktioilla)
C:
cd "%SIJOITTELUFOLDER%\Database"
@rem
@rem Tuhotaan hakemistossa mahdollisesti jo olevat tiedostot jakoluvut.EImax ja vastusmatriisit.EIsum
DEL jakoluvut.EImax vastusmatriisit.EIsum
@rem Tuhotaan hakemistossa mahdollisesti jo olevat "vastus*tayd*.txt" -tiedostot
@rem seka ha-, kevyt ja ruuhkamaksu -.txt -tiedostot (ha*vastus.txt)
REM *** DEL ha*vastus.txt vastus*tayd*.txt
@rem
@rem Poistetaan vanhat ha- ja jkl-matkamatriisit ja kopioidaan uudet ennustepankista
Emme -ng -m matin.mac  d311_del_ha_ja_jl_kysyntaW.in
Emme -ng -m import.mac %ENNUSTEFOLDER% mf01 mf06
@REM
@rem Kaynnistetaan Emme sijoittelupankissa suoraan makroon, joka tekee kaiken tarvittavan
Emme -ng -m aja_sisajo_loppu.mac  EI  %2
Emme -ng -m ajatrass_perus_M2016.mac
Emme -ng -m AJA_LOPUT_M2016.MAC  EI
"%EMMEPATH%\Python27\python.exe" hankearvdata.py %SIJOITTELUFOLDER%\Database
@rem 
C:
cd "%ENNUSTEFOLDER%\Database"
ECHO Viimeinen sijoittelu ennustetuilla matriiseilla ajettu >> bat_loki_ka.txt
@date /t >> bat_loki_ka.txt
@time /t >> bat_loki_ka.txt
@ECHO OFF
@rem
CD ..\..
ECHO.Ennusteprosessi on ajettu loppuun. Paina jotain nappulaa sulkeaksesi komentoikkunan.
GOTO LOPPU 
@rem
:VIRHE
ECHO Anna parametrina kierrosten maara (vahintaan 2)
@rem
:LOPPU
PAUSE
