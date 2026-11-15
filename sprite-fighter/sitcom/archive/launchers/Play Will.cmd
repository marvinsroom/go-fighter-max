@echo off
cd /d "%~dp0engine\ikemen-go-v1.0.0"
start "" "Ikemen_GO.exe" -loadmotif -p1 will_full -p2 will_full -p1.ai 0 -p2.ai 0 -p1.power 3000 -p2.power 3000 -s stages/stage0-720.def -time 99
