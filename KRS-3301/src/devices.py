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
# Project import
import modules.device.extr_Scaler_IN806_IN1808_Series_v1_1_6_0 as modScalar
import modules.device.epsn_vp_CB_EB_PowerLite_L630U_Series_v1_0_4_0 as Projector


# Define devices
dvIPCP = ProcessorDevice('KRS-3301-IPCP')
dvTLP = UIDevice('KRS-3301-TLP')


#connecting the devices to eachother

#TODO - figure out connection through DTP device
dvScalar = modScalar.SSHClass('10.10.2.30', 22023, Model='IN1808 IPCP Q MA')


dvPRJ = Projector.SerialOverEthernetClass('10.10.2.30', 2003, Model='CB-L630U') # Figure out numbers needed for this device connection




