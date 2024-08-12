@echo off
cd /d "%~dp0"
powershell -Command "Start-Process pythonw -ArgumentList 'hotspot_guardian_at' -Verb RunAs"