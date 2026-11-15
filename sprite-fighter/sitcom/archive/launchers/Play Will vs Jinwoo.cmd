@echo off
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "..\scripts\run-will-vs-jinwoo.ps1" -Mode Play
