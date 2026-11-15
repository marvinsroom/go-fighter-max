@echo off
cd /d "%~dp0engine\ikemen-go-v1.0.0"
start "" "Ikemen_GO.exe" -p1 will_motion -p2 will_motion -p1.ai 0 -p2.ai 0 -s stages/stage0-720.def -time -1
