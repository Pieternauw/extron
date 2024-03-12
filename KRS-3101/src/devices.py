"""
This is the place to define each of the devices in the system.
* Extron control devices (e.g. all extronlib.device objects)
* Non-control devices and services (e.g. device modules)
* User defined devices (e.g. all extronlib.interface objects or custom python coded devices)

Note: This is for definition only.  Connection and logic defined in system.py (see below).
"""

# Python imports

# Extron Library imports
from extronlib.device import ProcessorDevice, UIDevice

# Project imports
import modules.device.extr_Scaler_IN806_IN1808_Series_v1_1_6_0 as modScalar
import modules.device.epsn_vp_CB_EB_PowerLite_L630U_Series_v1_0_4_0 as Projector
import modules.device.tasc_bluray_BD_MP4K_v1_0_0_0 as Bluray

# Define devices
dvIPCP = ProcessorDevice('KRS-3101-IPCP')
dvTLP = UIDevice('KRS-3101-TLP')

dvScalar = modScalar.SSHClass('10.10.2.30', 22023, Model='IN1808 IPCP MA 70')

dvBluray = Bluray.SerialClass(dvIPCP, 'COM1', Model='BD-MP4k') 

dvPRJ = Projector.SerialOverEthernetClass('10.10.2.30', 2003, Model='CB-L630U') # Figure out numbers needed for this device connection


"""NOTE Devices that don't connect will cause the program to go on an inf. loop
        Maybe limit the while loop to 5 attempts
        Could also be a good way to tell if a declaration is wrong, just which one is all

def ConnectDevice(device):
    result = device.Connect(5)
    while 'Connected' not in result:
        Wait(5, device.Connect(5))

def Initialize():
    ConnectDevice(dvScalar)
    ConnectDevice(dvBluray)
    ConnectDevice(dvPRJ)
"""


