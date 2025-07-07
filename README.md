The purpose of this project is to restore the functionality of six buttons on the McDonald Observatory 82" Telescope Console that control the dome slit and curtains.

# Program Description
Every 0.5s, the Pi reads the buttons, checks for conflicts or direction reversals, then sends commands over the network to the web relay that controls the dome slit and curtains.

## Initial state
First, each of the pins are assigned according to the GPIO labels on the Raspberry Pi. Each pin is also set to "pull down" to make them default to LOW (False).

Next, all the http commands are assigned. These are the commands that are sent to the web relay controller, which in turns opens and closes the relays that control the dome slit and curtains. (For testing, the http commands are replaced with normal print statements.)

Finally, all button states and previous button states are defaulted to "False", and then the main while loop begins, looping every 0.5s.

## The main while loop
Runs every 0.5s and does the following:
1. Calls buttons_check_all() to check all the GPIO inputs and store the inputs as the current state of the buttons.
2. Check if two disallowed buttons are being pressed at the same time (eg, both lowering and raising the upper curtain). Set curtain_flag if so.
3. Check if a direction is being quickly reversed by comparing the current button input with the previous button input. Set direction_flag if so.
4. If curtain_flag or direction_flag is true, do not send any commands. Additionally, store the inputs as "previous" inputs for the next round.
5. If all checks are passed, send the commands using send_cmd(). Additionally, store the inputs as "previous" inputs for the next round.
 
## send_cmd()
send_cmd() takes the following information for a button:
1. The previous state of the button
2. The current state of the button
3. The button's "relay down" command (for "button pressed")
4. The button's "relay up" command (for "button released")
 
send_cmd() then sends one of two commands for each button:
1. If the button is being pressed, send the "button is pressed" command
2. If the button was previously being pressed, but now it is not, send the "button is released" command.

send_cmd() returns the current state of the button to be stored as the previous state of the button for the next round.

# Raspberry Pi GPIO
* GPIO 13 : Dome slit close
* GPIO 27 : Dome slit open
* GPIO 17 : Upper curtain drop
* GPIO 24 : Upper curtain raise
* GPIO 22 : Lower curtain drop
* GPIO 20 : Lower curtain raise

![pi_GPIO](pi_GPIO.png)
