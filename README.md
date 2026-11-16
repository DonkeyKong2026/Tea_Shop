Week Update 1:

You vibescode.py, vibecode.py and the musicwithstyle.py are the music running code for the output setup.


Week Update 2:

The new additions of the code include stepperrotate.py, RGB.py, mcp9808_mod.py, HEATER.py, claw.py

stepperrotate.py: 
rotates the stepper for the turn table, it rotates the table 90 degrees then stops and waits in idle, steps have been put into place so that when a task is completed i.e finishing a dispensing, the table will turn to the next, however until those functions are complete for now the code only rotates the turntable 90 degrees.

RGB.py
Changes the LED to describe the temperature of its surroundings, green meaning cold, yellow meaning warm, and red meaning hot. The code works with a single 4pronged multicolor LED and a mcp9808 temperature sensor.

claw.py
claw.py rotates the initial claw design with the stepper motor, it will be repurposed for the salt shaker code but for now as our current state we will hold it here for further editing.

HEATER.py
This code drives the heating pad with the help of a 12W power supply, using a pi and the DM3 driver we control the on and off states of the temperature pads which are wired in series. 

mcp9808_mod.py
This code holds the main class functions for the mcp9808, it's a supporting code to the temperature plate as the code needs to be present in the same folder in order for RGB.py to know what python functions to call.

