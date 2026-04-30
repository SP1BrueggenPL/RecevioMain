#Requires AutoHotkey v2.0
#SingleInstance Force
Persistent(true)

; 🔒 BLOKADA NAJWAŻNIEJSZYCH SKRÓTÓW
!F4::return
!Tab::return
^!Delete::return
^Esc::return
#d::return
#r::return
#e::return
#x::return
#i::return
LWin::return
RWin::return
^+Esc::return
^!Del::return
^+Del::return

; 🔒 BLOKADA ZMIANY WIRTUALNYCH PULPITÓW
#Left::return
#Right::return

; 🔒 BLOKADA MENU KONTEKSTOWEGO
AppsKey::return

; 🔒 BLOKADA F1–F12 (w tym F11 – jeden zapis)
F1::return
F2::return
F3::return
F4::return
F5::return
F6::return
F7::return
F8::return
F9::return
F10::return
F11::return
F12::return

; ✅ BLOKADA ALT+SPACJA
!Space::return
