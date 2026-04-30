@echo off
set svc=QRConference_Service
set port=8000

REM 1) grzeczne zatrzymanie usługi
sc stop %svc% >nul 2>&1
timeout /t 2 >nul

REM 2) zabicie wszystkiego uruchomionego przez usługę (jeśli jeszcze żyje)
taskkill /F /T /FI "SERVICES eq %svc%" >nul 2>&1

REM 3) zabicie procesu nasłuchującego na porcie (działa PL/EN, IPv4/IPv6)
for /f "tokens=5" %%p in ('
  netstat -aon ^| findstr /i ":%port%" ^| findstr /i /v "UDP"
') do (
  taskkill /F /T /PID %%p >nul 2>&1
)

exit /b 0
