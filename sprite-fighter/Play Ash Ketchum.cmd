@echo off
cd /d "%~dp0engine\ikemen-go-v1.0.0"
start "" "Ikemen_GO.exe" -config save/config.ini -loadmotif -p1 ash-ketchum -p2 baam -p1.ai 0 -p2.ai 8 -s stages/stage0-720.def
