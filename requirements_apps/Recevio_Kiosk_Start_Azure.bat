@echo off

:: Recevio - uruchomienie kiosku wskazujacego na wdrozenie Azure (bez lokalnego serwera Django)

:: Uruchomienie AutoHotkey z blokada wyjscia (Alt+F4, Alt+Tab, Win, Esc, menu kontekstowe itd.)
start "" "C:\Program Files\AutoHotkey\UX\kiosk_block.ahk"

:: Uruchom Microsoft Edge w trybie kiosku (fullscreen) na adresie Azure
start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --kiosk https://recevio-hpf4fxddh7ckc7gm.westeurope-01.azurewebsites.net/start --edge-kiosk-type=fullscreen --no-first-run --no-default-browser-check --noerrdialogs --disable-session-crashed-bubble

exit
