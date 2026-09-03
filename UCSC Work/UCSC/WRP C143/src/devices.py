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
from extronlib.interface import EthernetClientInterface
# Project imports
import modules.device.epsn_vp_CB_EB_PowerLite_L630U_Series_v1_0_4_0 as DPRJ 
#import modules.device.epsn_vp_CB_EB_Powerlite_L730U_Series_v1_0_4_0 as SPRJ
from modules.helper.ConnectionHandler import GetConnectionHandler
from modules.helper.ModuleSupport import eventEx

# Define devices

dvIPCP = ProcessorDevice('ProcessorAlias')
dvDNBP = UIDevice('DoublePRJ')

dvDPRJDoor = GetConnectionHandler(DPRJ.EthernetClass('10.10.2.40', 3629), 'Power', pollFrequency=30)
dvDPRJWall = GetConnectionHandler(DPRJ.EthernetClass('10.10.2.41', 3629), 'Power', pollFrequency=30)

@eventEx([dvDPRJDoor, dvDPRJWall], ['Connected', 'Disconned'])
def ProjectorConnected(client:EthernetClientInterface, state):
    print('Device on IP {0} is {1}'.format(client.IPAddress, state))
    if state is 'Connected':
        client.Update('Power')
        client.Update('AVMute')