 
.\sqlite3.exe game.db "update buildable_health set health_percentage=1 where object_id in ( SELECT object_id FROM buildings where owner_id=(SELECT guildId from guilds where name='GM') )"
::.\sqlite3.exe game.db "select health_percentage from  buildable_health  where object_id in ( SELECT object_id FROM buildings where owner_id=(SELECT guildId from guilds where name='GM') );"

pause