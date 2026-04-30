@echo off
cd /d C:\GuestBook
call myvenv\Scripts\activate.bat

:: Uruchomienie serwera Django w tle, bez okna CMD
start "" /B C:\GuestBook\myvenv\Scripts\python manage.py process_tasks


exit
