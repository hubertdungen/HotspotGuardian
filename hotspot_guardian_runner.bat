REM @echo off
REM cd /d "%~dp0"
REM powershell -Command "Start-Process pythonw -ArgumentList 'hotspot_guardian_at' -Verb RunAs"

REM @echo off
REM powershell Start-Process pythonw -ArgumentList '"%~dp0hotspot_guardian.pyw"' -Verb RunAs


REM @echo off
REM powershell -Command "Start-Process pythonw -ArgumentList '%~dp0hotspot_guardian.pyw' -Verb RunAs -WindowStyle Hidden"




@echo off
REM Run the Python script to manage the hotspot
pythonw.exe hotspot_guardian_v2.pyw

REM Ensure the command is run with elevated privileges
powershell -Command "Start-Process -FilePath 'pythonw.exe' -ArgumentList 'hotspot_guardian_v2.pyw' -Verb runAs"
exit