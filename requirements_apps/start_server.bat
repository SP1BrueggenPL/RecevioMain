@echo off
cd /d C:\GuestBook
call myvenv\Scripts\activate.bat

:: Uruchomienie serwera Django w tle
start "" /B C:\GuestBook\myvenv\Scripts\python.exe manage.py runserver 0.0.0.0:8000

:: Poczekaj 5 sekund na start serwera
timeout /t 5 >nul

:: Uruchomienie AutoHotkey z blokadą wyjścia (Alt+F4, Alt+Tab itd.)
start "" "C:\Program Files\AutoHotkey\UX\kiosk_block.ahk"

:: Uruchom Microsoft Edge w trybie kiosku (fullscreen)
start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --kiosk http://localhost:8000/start --edge-kiosk-type=fullscreen

exit
