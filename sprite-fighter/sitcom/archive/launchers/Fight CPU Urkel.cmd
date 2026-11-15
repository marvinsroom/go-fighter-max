@echo off
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "..\scripts\run-will-vs-urkel.ps1" -Mode CPU
