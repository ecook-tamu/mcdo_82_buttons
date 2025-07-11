import RPi.GPIO as GPIO
import time
import requests

########################################################################
#
# First, each of the pins are assigned according to the GPIO labels on
# the Raspberry Pi. Each pin is also set to "pull down" to make them
# default to LOW (False).
#
# Next, all the http commands are assigned. These are the commands that
# are sent to the web relay controller, which in turns opens and closes
# the relays that control the dome slit and curtains.
#
# For testing, the http commands are replaced with normal print statements.
# The http commands are in a separate document.
#
# The class "PiButtons" contains all the code for reading the GPIO inputs,
# deciding if the inputs are allowable, and sending the http commands.
#
#
# The main while loop runs every 0.5s and does the following:
# 1. Calls buttons_check_all() to check all the GPIO inputs and
#    store the inputs as the current state of the buttons.
# 2. Check if two disallowed buttons are being pressed at the same
#    time (eg, both lowering and raising the upper curtain).
#    Set curtain_flag if so.
# 3. Check if a direction is being quickly reversed by comparing the
#    current button input with the previous button input.
#    Set direction_flag if so.
# 4. If curtain_flag or direction_flag is true, do not send any commands.
#    Additionally, store the inputs as "previous" inputs for the next round.
# 5. If all checks are passed, send the commands using send_cmd()
#    Additionally, store the inputs as "previous" inputs for the next round.
#
# 
# send_cmd() takes the following information for a button:
# 1. The previous state of the button
# 2. The current state of the button
# 3. The button's "relay down" command (for "button pressed")
# 4. The button's "relay up" command (for "button released")
# 
# send_cmd() then sends one of two commands for each button:
# 1. If the button is being pressed, send the "button is pressed" command
# 2. If the button was previously being pressed, but now it is not,
#    send the "button is released" command.
#
# send_cmd() returns the current state of the button to be stored
# as the previous state of the button for the next round.
#
########################################################################

# Sets Raspberry Pi pins to match the GPIO labels
GPIO.setmode(GPIO.BCM)

# Assign GPIO pins on the Raspberry Pi
PIN_dome_close  = 13
PIN_dome_open   = 27
PIN_upper_drop  = 17
PIN_upper_raise = 24
PIN_lower_drop  = 22
PIN_lower_raise = 20

# Sets Raspberry Pi pins to default to a LO state
GPIO.setup(PIN_dome_close,  GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(PIN_dome_open,   GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(PIN_upper_raise, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(PIN_upper_drop,  GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(PIN_lower_raise, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(PIN_lower_drop,  GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

########################################################################
#
# for testing, the commands are just strings that print to the console
# refer to separate google doc for http commands
#
########################################################################

# DOME SLIT:
dome_close_relay_command_down  = "close dome button is pressed"
dome_close_relay_command_up    = "close dome button is released"
dome_open_relay_command_down   = "open dome button  is pressed"
dome_open_relay_command_up     = "open dome button  is released"

# UPPER CURTAIN:
uc_close_relay_command_down    = "drop upper curtain button  is pressed"
uc_close_relay_command_up      = "drop upper curtain button  is released"
uc_open_relay_command_down     = "raise upper curtain button is pressed"
uc_open_relay_command_up       = "raise upper curtain button is released"

# LOWER CURTAIN:
lc_close_relay_command_down    = "drop lower curtain button  is pressed"
lc_close_relay_command_up      = "drop lower curtain button  is released"
lc_open_relay_command_down     = "raise lower curtain button is pressed"
lc_open_relay_command_up       = "raise lower curtain button is released"

class PiButtons:
    def __init__(self):
        # All buttons begin in the "not pressed" state
        self.button_dome_close   = False
        self.button_dome_open    = False
        self.button_upper_drop   = False
        self.button_upper_raise  = False
        self.button_lower_drop   = False
        self.button_lower_raise  = False
        
        # All buttons begin in the "not previously pressed" state
        self.prev_button_dome_close   = False
        self.prev_button_dome_open    = False
        self.prev_button_upper_drop   = False
        self.prev_button_upper_raise  = False
        self.prev_button_lower_drop   = False
        self.prev_button_lower_raise  = False
        
    # Every 0.5s, check the state of each button
    def button_check_all(self):
        self.button_dome_close   = GPIO.input(PIN_dome_close)
        self.button_dome_open    = GPIO.input(PIN_dome_open)
        self.button_upper_drop   = GPIO.input(PIN_upper_drop)
        self.button_upper_raise  = GPIO.input(PIN_upper_raise)
        self.button_lower_drop   = GPIO.input(PIN_lower_drop)
        self.button_lower_raise  = GPIO.input(PIN_lower_raise)
    
    # Every 0.5s, send the BUTTON PRESSED/RELEASED commands depending on
    # the current state of the button and the previous state of the button
    def send_cmd(self, prev, button, cmd_down, cmd_up):
        # If the button is being pressed, send the BUTTON PRESSED command
        if button:
            #response = requests.get(cmd_down)
            #print(response)
            print(cmd_down)
            
        # If the button is not being pressed, check the previous state of the button
        # If the button was previously being pressed, send the BUTTON RELEASED command
        else:
            if prev:
                #response = requests.get(cmd_up)
                #print(response)
                print(cmd_up)
        # return the state of the button for the next round
        return button
        
    def run(self):
        while (True):
            # These flags ensure two conflicting buttons aren't being pressed
            # and check if the direction of the dome slit or curtains are reversing
            curtain_flag = False
            direction_flag = False
            
            # Check all the buttons
            self.button_check_all()
            
            # Check if the curtain buttons are being pressed at the same time
            if self.button_upper_raise and self.button_upper_drop:
                print("Cannot raise and drop upper curtain at the same time")
                curtain_flag = True
                
            if self.button_lower_raise and self.button_lower_drop:
                print("Cannot raise and drop lower curtain at the same time")
                curtain_flag = True
             
            # If the curtain is flagged, skip the direction checks
            if not curtain_flag:
                # Check each button to see if a direction is being reversed
                
                # Reversing the dome slit direction
                if self.prev_button_dome_close  and self.button_dome_open:
                    print("Reversing dome slit direction")
                    direction_flag = True
                if self.prev_button_dome_open   and self.button_dome_close:
                    print("Reversing dome slit direction")
                    direction_flag = True
                    
                # Reversing the upper curtain direction
                if self.prev_button_upper_raise and self.button_upper_drop:
                    print("Reversing upper curtain direction")
                    direction_flag = True
                if self.prev_button_upper_drop  and self.button_upper_raise:
                    print("Reversing upper curtain direction")
                    direction_flag = True
                    
                # Reversing the lower curtain direction
                if self.prev_button_lower_raise and self.button_lower_drop:
                    print("Reversing lower curtain direction")
                    direction_flag = True
                if self.prev_button_lower_drop  and self.button_lower_raise:
                    print("Reversing lower curtain direction")
                    direction_flag = True
                
            # If all the checks are passed, commands can be sent.
            # Otherwise, this round is skipped, the prev states are updated, and an extra 0.5s wait is imposed
            if curtain_flag or direction_flag:
                self.prev_button_dome_close   = self.button_dome_close
                self.prev_button_dome_open    = self.button_dome_open
                self.prev_button_upper_drop   = self.button_upper_drop
                self.prev_button_upper_raise  = self.button_upper_raise
                self.prev_button_lower_drop   = self.button_lower_drop
                self.prev_button_lower_raise  = self.button_lower_raise
                print("Skipping this round due to curtain or direction flag")
                
                time.sleep(0.5)
                
            else:
                # The previous state of the button, the current state of the button, the pressed command, and the released command
                # are sent to the send_cmd function, which compares the states and sends the commands
                self.prev_button_dome_close  = self.send_cmd(self.prev_button_dome_close,  self.button_dome_close,  dome_close_relay_command_down, dome_close_relay_command_up)
                self.prev_button_dome_open   = self.send_cmd(self.prev_button_dome_open,   self.button_dome_open,   dome_open_relay_command_down,  dome_open_relay_command_up)
                self.prev_button_upper_drop  = self.send_cmd(self.prev_button_upper_drop,  self.button_upper_drop,  uc_close_relay_command_down,   uc_close_relay_command_up)
                self.prev_button_upper_raise = self.send_cmd(self.prev_button_upper_raise, self.button_upper_raise, uc_open_relay_command_down,    uc_open_relay_command_up)
                self.prev_button_lower_drop  = self.send_cmd(self.prev_button_lower_drop,  self.button_lower_drop,  lc_close_relay_command_down,   lc_close_relay_command_up)
                self.prev_button_lower_raise = self.send_cmd(self.prev_button_lower_raise, self.button_lower_raise, lc_open_relay_command_down,    lc_open_relay_command_up)
            
            time.sleep(0.5) # wait 0.5 seconds
            
pi_buttons = PiButtons()
pi_buttons.run()
