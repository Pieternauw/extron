"""
The system is the place to define system logic, automation, services, etc. as a whole.  It should
provide an *Initialize* method that will be called in main to start the start the system after
variables, devices, and UIs have been defined.

Examples of items in the system file:
* Clocks and scheduled things
* Connection of devices that need connecting
* Set up of services (e.g. ethernet servers, CLIs, etc.)
"""

# Python imports

# Extron Library imports
import devices
# Project imports

def Initialize():
    # Connect all devices
    devices.dvMatrix.Connect()
    print('connecting matrix')
    #devices.dvLeftPRJ.Connect()
    #devices.dvRightPRJ.Connect()
    devices.dvCenterPRJ.Connect()
    print('connecting prj')
    devices.dvBluray.Connect()
    print('connecting bluray')
    devices.dvBiamp.Connect()
    print('connecting biamp')
    devices.dvTLPMain.HideAllPopups()
    devices.dvTLPMain.ShowPage('Start Page')
    # Finish Initialize() with a print()
    print('System Initialized')
