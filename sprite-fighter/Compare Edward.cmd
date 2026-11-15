@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0..\scripts\run-edward-fighter.ps1" -Mode Compare
