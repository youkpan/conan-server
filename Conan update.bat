@ECHO OFF

color 03

ECHO Updating SteamCMD and Server Files

steamcmd +login anonymous +force_install_dir "C:\conan\server" +app_update 443030 +quit

@ECHO OFF

cd C:\conan\server

ECHO Starting Conan Exiles Server

ConanSandboxServer.exe -log 
#rem -QueryPort=27017

exit