# mcdo_82_console
The purpose of this project is to restore the functionality of six buttons on the McDonald Observatory 82" Telescope Console that control the dome slit and curtains.
https://instrumentation.tamu.edu/mcdo-82-console/

A Raspberry Pi is connected to the six buttons:
* Pin 11 : Dome slit close
* Pin 13 : Dome slit open
* Pin 15 : Upper curtain drop
* Pin 16 : Upper curtain raise
* Pin 18 : Lower curtain drop
* Pin 22 : Lower curtain raise
Every 0.5s, the Pi reads the buttons, checks for conflicts or direction reversals, then sends the URL commands to the web relay that controls the dome slit and curtains. It stores the state of the button to be compared to for the next 0.5s check.
