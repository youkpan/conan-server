
@echo off
:::::::::::::::::::::::::::::::::::::
:: MODS IDs
:::::::::::::::::::::::::::::::::::::
:::: CHANGE ModDownload to True
:::: if you wish to download.
:::::::::::::::::::::::::::::::::::::
::::RHS MODS
:::::::::::::::::::::::::::::::::::::
set ModsName[0]=Pippi
set Mods[0]=880454836
set ModDownload[0]=true

:::::::::::::::::::::::::::::::::::::
set ModsName[1]=TheColdEmbrace-Main
set Mods[1]=1113901982
set ModDownload[1]=true

:::::::::::::::::::::::::::::::::::::
set ModsName[2]=LitManItemStackAndContainerSize
set Mods[2]=1125427722
set ModDownload[2]=true
:::::::::::::::::::::::::::::::::::::
set ModsName[3]=300
set Mods[3]=1386174080
set ModDownload[3]=true

:::::::::::::::::::::::::::::::::::::
::::MASSI MODS
:::::::::::::::::::::::::::::::::::::
set ModsName[4]=RA
set Mods[4]=1542041983
set ModDownload[4]=true

:::::::::::::::::::::::::::::::::::::
set ModsName[5]=Improved_Quality_of_Life
set Mods[5]=1657730588
set ModDownload[5]=true

:::::::::::::::::::::::::::::::::::::
set ModsName[6]=DungeonMasterTools
set Mods[6]=1699858371
set ModDownload[6]=true

:::::::::::::::::::::::::::::::::::::
set ModsName[7]=Tutorial
set Mods[7]=1734383367
set ModDownload[7]=true

:::::::::::::::::::::::::::::::::::::
set ModsName[8]=NumericHUD
set Mods[8]=1753303494
set ModDownload[8]=true

:::::::::::::::::::::::::::::::::::::
set ModsName[9]=EEWAExtraFeatLightsabers
set Mods[9]=1795327310
set ModDownload[9]=true 


:::::::::::::::::::::::::::::::::::::
set ModsName[10]=StylistPlus
set Mods[10]=1159180273
set ModDownload[10]=true 


:::::::::::::::::::::::::::::::::::::
:::: MODS ID END ^^^^^^^^^^^^^^^^^^^^
:::::::::::::::::::::::::::::::::::::


echo This Will Install/Update Arma3 Mods
echo.
echo Author: Joew
echo Credits: tinboye - www.fortex.wtf - Gives me the cmd to update mods.
echo.

:: STEAM CONFIGS

::Path to SteamCMD.exe without \
set "steamcmdpath=C:\conan"

:: OPTION 1: ASKING FOR STEAM LOGIN AND PASS

::set /p login=Steam Login: 
::echo.
::set /p pass=Steam Pass: 
::echo.

:: END OPTION 1

:: OPTION 2: Set your steam and pass and save it. (I don't recommend this for security)

set "login=teluwl"
set "pass=Pan7777777"
set "mods_install=%steamcmdpath%\Mods"

:: END OPTION 2

:: END STEAM CONFIGS

:: Folder Mods => SteamCMD\steamapps\workshop\content\107410

set "x=0"

del %steamcmdpath%\server\ConanSandbox\Mods\modlist1.txt
del %steamcmdpath%\server\ConanSandbox\Mods\modlist2.txt

:SymLoop
if defined Mods[%x%] (
if defined ModDownload[%x%] (
if defined ModsName[%x%] (

call set "name=%%ModsName[%x%]%%"
call set "id=%%Mods[%x%]%%"
call set "downloads=%%ModDownload[%x%]%%"
if "%downloads%"=="true" (
cls
echo Downloading the Mod: %name% - ID: %id%
echo.
::pause
echo.
%steamcmdpath%\steamcmd +login %login% %pass% +force_install_dir "%mods_install%" +"workshop_download_item 440900 %id%" +quit
::move %steamcmdpath%\server\ConanSandbox\Mods\steamapps\workshop\content\440900\%id%\* %steamcmdpath%\server\ConanSandbox\Mods\
::echo "mklink /H %steamcmdpath%\server\ConanSandbox\Mods\%name%.pak %mods_install%\steamapps\workshop\content\440900\%id%\%name%.pak"
echo *%mods_install%\steamapps\workshop\content\440900\%id%\%name%.pak >> %steamcmdpath%\server\ConanSandbox\Mods\modlist1.txt
::echo *%name%.pak >> %steamcmdpath%\server\ConanSandbox\Mods\modlist2.txt
::pause
)
)
)
set /a "x+=1"
GOTO :SymLoop
)
pause