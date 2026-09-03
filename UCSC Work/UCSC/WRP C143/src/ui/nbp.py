"""
This is the place to put the modules for each UI in the system.  One module for each unique ui --
mirrored panels should be in the same file.
* UI object definition
* UI navigation
"""

# Python imports

# Extron Library imports
from extronlib.ui import Button
from extronlib.system import MESet 
# Project imports
from modules.helper.ModuleSupport import eventEx 
from devices import dvDNBP
# Define UI Objects
btn_doorOn = Button(dvDNBP, 60041)
btn_doorOff = Button(dvDNBP, 60042)
btn_doorMute = Button(dvDNBP, 60034)

btn_wallOn = Button(dvDNBP, 60044)
btn_wallOff = Button(dvDNBP, 60045)
btn_wallMute = Button(dvDNBP, 60046)

# Define UI Object Events
door_set = MESet([btn_doorOn, btn_doorOff])
wall_set = MESet([btn_wallOn, btn_wallOff])

for button in door_set.Objects:
    door_set.SetStates(button, 1, 2)
    
for button in wall_set.Objects:
    wall_set.SetStates(button, 1, 2)

@eventEx(door_set.Objects, 'Pressed')
@eventEx(wall_set.Objects, 'Pressed')
def PRJButton(button:Button, state):
    pass

@eventEx([btn_doorMute, btn_wallMute], 'Pressed')
def PRJMute(button:Button, state):
    pass