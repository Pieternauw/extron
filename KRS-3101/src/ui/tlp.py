"""
This is the place to put the modules for each UI in the system.  One module for each unique ui --
mirrored panels should be in the same file.
* UI object definition
* UI navigation
"""

# Python imports

# Extron Library imports
from extronlib import event
from extronlib.system import MESet
from extronlib.ui import Button, Level, Slider, Label

# Project imports
import variables
from modules.helper.ModuleSupport import eventEx
from devices import dvTLP, dvIPCP, dvScalar, dvPRJ
#bring in variables here for defaults (audio level, default source and what not)

# Define UI Objects
ButtonEventList = ['Pressed', 'Released', 'Held', 'Repeated', 'Tapped']

#Tap to start
btn_startScreen = Button(dvTLP, 19)

@event(btn_startScreen, 'Pressed')
def ShowStartPage(button, state):
    dvTLP.ShowPage("Main passcode")
    #may want to auto this to the main page if I can't get the passcode going before deployment
    


"""PASSCODE SCREEN"""

#opening the passcode file
file = open("passcode.txt", "r")
passcode = file.readline()
file.close

PadButtons = []
for Button_IDs in range(141, 151):
    PadButtons.append(Button(dvTLP, Button_IDs))
    
LblPadString = Label(dvTLP, 140)
PadString = ''

@event(PadButtons, ButtonEventList)
def PadButtonPressed(button, state):
    global PadString 
    if state == 'Pressed':
        button.SetState(1)
        PadString += button.Name
        LblPadString.SetText(PadString)
    elif state == 'Released':
        button.SetState(0)

#enter and clear
btn_passcodeEnter = Button(dvTLP, 152)
@event(btn_passcodeEnter, ButtonEventList)
def BtnEnterPasscode(button, state):
    global PadString 
    if state == 'Pressed':
        button.SetState(1)
        if PadString == '2748' or PadString == passcode:      #whatever the current passcode is
            PadString = ''
            LblPadString.SetText(PadString)
            dvTLP.ShowPage('Main Page')
        else:
            PadString = ''
            LblPadString.SetText(PadString)
    elif state == 'Released':
        button.SetState(0)

btn_passcodeClear = Button(dvTLP, 151)
@event(btn_passcodeClear, ButtonEventList)
def BtnClearPad(button, state):
    global PadString
    if state == 'Pressed':
        button.SetState(1)
        PadString = ''
        LblPadString.SetText(PadString)
    elif state == 'Released':
        button.SetState(0)
        
"""MAIN PAGE"""
#Source Selection  
btn_sourceHDMI = Button(dvTLP, 10)
btn_sourceWireless = Button(dvTLP, 16)
btn_sourceDocCam = Button(dvTLP, 14)
btn_sourceBluray = Button(dvTLP, 11)

input_set = MESet([btn_sourceHDMI, btn_sourceDocCam, btn_sourceBluray, btn_sourceWireless])

for button in input_set.Objects:
    input_set.SetStates(button, 0, 1)
    
input_set.SetCurrent(None)
    
#TODO - set up statements to check projector status when input switched (if not on turn on)
@eventEx(input_set.Objects, 'Pressed')
def SwitchInput(button, state):
    if button is  btn_sourceHDMI: # TODO setup for GetCurrent() - not neccessary since that seems to be live update which I don't need I only need on trigger of event
        dvScalar.Set('Input', '2', {'Type': 'Audio/Visual'})
        dvTLP.HideAllPopups()
        dvTLP.ShowPopup("Laptop Connected popup")
    elif button is btn_sourceWireless:
        dvScalar.Set('Input', '3', {'Type': 'Audio/Visual'})
        dvTLP.HideAllPopups()
        dvTLP.ShowPopup("Wireless instruction popup")
    elif button is btn_sourceDocCam:
        dvScalar.Set('Input', '4', {'Type': 'Audio/Visual'})
        dvTLP.HideAllPopups()
        dvTLP.ShowPopup("Document camera instruction popup")
    elif button is btn_sourceBluray:
        dvScalar.Set('Input', '5', {'Type': 'Audio/Visual'})      #need to activate com1 if using bluray controls (maybe not)
        dvTLP.HideAllPopups()
        dvTLP.ShowPopup("BluRay control popup")
        
    #turning on projector if it's off
    if dvPRJ.Update('Power') == 'Off':
        dvPRJ.Set('Power', 'On')
        #check to see if I need to do something with warming status 
    
    input_set.SetCurrent(button)

#Program audio control 

btn_progAudioUp = Button(dvTLP, 84)
btn_progAudioDown = Button(dvTLP, 83)
btn_progAudioMute = Button(dvTLP, 82)

#level bar
lvl_prog = Level(dvTLP, 18)
lvl_prog.SetRange(-100, 12, 2)     #In steps of 2

prog_val = -18

lvl_prog.SetLevel(prog_val)
dvScalar.Set('GroupProgramVolume', prog_val)

@event(btn_progAudioUp, ButtonEventList)
def ProgAudioUp(button, state):
    if state == 'Pressed':
        button.SetState(1)
        global prog_val

        lvl_prog.Inc()
        prog_val += 2
        #increment scalar audio with group program volume
        dvScalar.Set('GroupProgramVolume', prog_val)
    elif state == 'Released':
        button.SetState(0)

@event(btn_progAudioDown, ButtonEventList)
def ProgAudioDown(button, state):
    if state == 'Pressed':
        button.SetState(1)
        global prog_val 

        lvl_prog.Dec()
        prog_val -= 2

        dvScalar.Set('GroupProgramVolume', prog_val)

@event(btn_progAudioMute, ButtonEventList)
def ProgAudioMute(button, state):
    if state == 'Pressed':
        if dvScalar.Update('GroupProgramMute') == 'Off':
            button.SetState(1)
            dvScalar.Set('GroupProgramMute', 'On') 
        else:
            button.SetState(0)
            dvScalar.Set('GroupProgramMute', 'Off')

#Microphone Audio
btn_micAudioUp = Button(dvTLP, 87)
btn_micAudioDown = Button(dvTLP, 89)
btn_micAudioMute = Button(dvTLP, 88)

#level bar
lvl_mic = Level(dvTLP, 85)
lvl_mic.SetRange(-100, 12, 1)

mic_val = -18

lvl_mic.SetLevel(mic_val)
dvScalar.Set('GroupMicVolume', mic_val)

@event(btn_micAudioUp, ButtonEventList)
def MicAudioUp(button, state):
    if state == 'Pressed':
        button.SetState(1)
        global mic_val

        lvl_mic.Inc()
        mic_val += 1
        
        dvScalar.Set('GroupMicVolume', mic_val)
    elif state == 'Released':
        button.SetState(0)

@event(btn_micAudioDown, ButtonEventList)
def MicAudioDown(button, state):
    if state == 'Pressed':
        button.SetState(1)
        global mic_val 

        lvl_mic.Dec()
        mic_val -= 1

        dvScalar.Set('GroupMicVolume', mic_val)

@event(btn_micAudioMute, ButtonEventList)
def MicAudioMute(button, state):
    if state == 'Pressed':
        if dvScalar.Update('GroupMicMute') == 'Off':
            button.SetState(1)
            dvScalar.Set('GroupMicMute', 'On') 
        else:
            button.SetState(0)
            dvScalar.Set('GroupMicMute', 'Off')


#Help Button
#TODO - what does this do?
btn_help = Button(dvTLP, 90)

#video Mute
#TODO - Global Video mute
btn_videoMute = Button(dvTLP, 17)
@event(btn_videoMute, ButtonEventList)
def VideoMute(button, state):
    if state == 'Pressed':
        if dvScalar.Update('GlobalVideoMute') == 'Off':
            dvScalar.Set('GlobalVideoMute', 'On')
            button.SetState(1)
        else:
            button.SetState(0)
            dvScalar.Set('GlobalVideoMute', 'Off')

#advanced settings
btn_advSettings = Button(dvTLP, 41)
@event(btn_advSettings, ButtonEventList)
def ShowAdvancedSettingsPopup(button, state):
    if state == 'Pressed':
        button.SetState(1)
        dvTLP.ShowPopup("Advanced settngs")
    elif state == 'Released':
        button.SetState(0)

#Activity Timeout
btn_actTimeout = Button(dvTLP, 155)
@event(btn_actTimeout, ButtonEventList)
def DisableActivityTimeout(button, state):
    if state == 'Pressed':
        button.SetState(1)
        #TODO - get timeout setup - do something with the system to disable said act timeout.
        print("something to disable errors\n") 
    elif state == 'Released':
        button.SetState(0)

#Projector

btn_projOn = Button(dvTLP, 24)
@event(btn_projOn, ButtonEventList)
def TurnOnProjector(button, state):
    if state == 'Pressed':
        button.SetState(1)
        #TODO - again same thing as with input selection, determine state of projector and do something 
        if dvPRJ.Update('Power') == 'Off':
            dvPRJ.Set('Power', 'On')
    elif state == 'Released':
        button.SetState(0)

btn_projOff = Button(dvTLP, 25)
@event(btn_projOff, ButtonEventList)
def TurnOnProjector(button, state):
    if state == 'Pressed':
        button.SetState(1)
        #TODO - again same thing as with input selection, determine state of projector and do something 
        input_set.SetCurrent(None)  #turn off all inputs. 
        if dvPRJ.Update('Power') == 'On' or dvPRJ.Update('Power') == 'Warming':
            dvPRJ.Set('Power', 'Off')
            dvScalar.Set('Input', '1', {'Type': 'Audio/Visual'})
            #TODO - determine if i have to wait for it to stop warming first
            
    elif state == 'Released':
        button.SetState(0)

btn_blankImg = Button(dvTLP, 21)
@event(btn_blankImg, ButtonEventList)
def BlankImage(button, state):
    if state == 'Pressed':
        button.SetState(1)
        if dvPRJ.Update('AVMute') == 'On':
            dvPRJ.Set('AVMute', 'Off')
        else:
            dvPRJ.Set('AVMute', 'On')

#Technician Access Code
TechButtons = []
for Button_IDs in range(107, 117):
    TechButtons.append(Button(dvTLP, Button_IDs))
    
LblTechString = Label(dvTLP, 20)
techstr = ''

@event(TechButtons, ButtonEventList)
def TechButtonPressed(button, state):
    global techstr 
    if state == 'Pressed':
        button.SetState(1)
        techstr += button.Name
        LblTechString.SetText(techstr)
    elif state == 'Released':
        button.SetState(0)

btn_techClear = Button(dvTLP, 117)
@event(btn_techClear, ButtonEventList)
def BtnClearTech(button, state):
    global techstr 
    if state == 'Pressed':
        button.SetState(1)
        techstr = ''
        LblTechString.SetText(techstr)
    elif state == 'Released':
        button.SetState(0)
        
btn_techEnter = Button(dvTLP, 118)
@event(btn_passcodeClear, ButtonEventList)
def BtnEnterTech(button, state):
    global techstr 
    if state == 'Pressed':
        button.SetState(1)
        if techstr == '2748':
            techstr = '' 
            LblTechString.SetText(techstr)
            dvTLP.ShowPopup('Audio Mix popup')
        else:
            techstr = ''
            LblTechString.SetText(techstr)
    elif state == 'Released':
        button.SetState(0)

#Advanced Exit 
btn_advSettingsExit = Button(dvTLP, 56)
@event(btn_advSettingsExit, ButtonEventList)
def ExitAdvancedSettingsPopup(button, state):
    if state == 'Pressed':
        global techstr
        button.SetState(1)
        techstr = ''
        LblTechString.SetText(techstr)          #clear the passcode before closing the page so it's empty when the user returns 
        dvTLP.HidePopup("Advanced settings")
    elif state == 'Released':
        button.SetState(0)

"""Audio Mix Popup"""
#Sliders
sld_lavMic = Slider(dvTLP, 22)
sld_lavMic.SetRange(-18, 80, 1)
@event(sld_lavMic, 'Changed')
def LavSlider(slider, state, value):
    if state == 'Changed':
        slider.SetFill(value)
        dvScalar.Set('MicLineInputGain', value, {'Input': '1'}) #TODO - Figure out if Lav is 1 or 2


sld_handHeld = Slider(dvTLP, 28)
sld_handHeld.SetRange(-18, 80, 1)   #TODO Check these numbers
@event(sld_handHeld, 'Changed')
def HandHeldSlider(slider, state, value):
    if state == 'Changed':
        slider.SetFill(value)
        dvScalar.Set('MicLineInputGain', value, {'Input': '2'})

sld_laptop = Slider(dvTLP, 35)
sld_laptop.SetRange(-18, 24, 0.5)     #TODO Check these numbers
@event(sld_laptop, 'Changed')
def LaptopSlider(slider, state, value):
    if state == 'Changed':
        slider.SetFill(value)
        dvScalar.Set('EmbeddedInputGain', value, {'Input': '1'})

sld_wireless = Slider(dvTLP, 39)
sld_wireless.SetRange(-18, 24, 0.5)     #TODO Check numbers
@event(sld_wireless, 'Changed')
def WirelessSlider(slider, state, value):
    if state == 'Changed':
        slider.SetFill(value)
        dvScalar.Set('EmbeddedInputGain', value, {'Input': '2'})

sld_bluray = Slider(dvTLP, 45)
sld_bluray.SetRange(-18, 24, 0.5)     #TODO Check numbers
@event(sld_bluray, 'Changed')
def BluraySlider(slider, state, value):
    if state == 'Changed':
        slider.SetFill(value)
        dvScalar.Set('EmbeddedInputGain', value, {'Input': '3'})

sld_ampLevelOut = Slider(dvTLP, 52)
sld_ampLevelOut.SetRange(-100, 0, 1)
@event(sld_ampLevelOut, 'Changed')
def AmpLevelSlider(slider, state, value):
    if state == 'Changed':
        slider.SetFill(value)
        dvScalar.Set('OutputAttenuation', value, {'Output': 'Amp Out'})

btn_exitMix = Button(dvTLP, 76)
@event(btn_exitMix, ButtonEventList)
def ExitAudioMix(button, state):
    if state == 'Pressed':
        button.SetState(1)
        dvTLP.HidePopup('Audio Mix popup')
    elif state == 'Released':
        button.SetState(0)


"""HDMI Popup"""
#Help Buttons
btn_macHelp = Button(dvTLP, 131)
@event(btn_macHelp, ButtonEventList)
def ShowMacHelpPopup(button, state):
    if state == 'Pressed':
        button.SetState(1)
        dvTLP.ShowPopup("mac laptop & tablet help popup")
    elif state == 'Released':
        button.SetState(0)
        

btn_winHelp = Button(dvTLP, 130)
@event(btn_winHelp, ButtonEventList)
def ShowMacHelpPopup(button, state):
    if state == 'Pressed':
        button.SetState(1)
        dvTLP.ShowPopup("Windows Laptop Help popup")
    elif state == 'Released':
        button.SetState(0)

"""Mac Help Popup"""
btn_exitMacHelp = Button(dvTLP, 58)
@event(btn_exitMacHelp, ButtonEventList)
def CloseMacHelpPopup(button, state):
    if state == 'Pressed':
        button.SetState(1)
        dvTLP.HidePopup("mac laptop & tablet help popup")
    elif state == 'Released':
        button.SetState(0)

"""Windows Help Popup"""
btn_exitWinHelp = Button(dvTLP, 163)
@event(btn_exitWinHelp, ButtonEventList)
def CloseMacHelpPopup(button, state):
    if state == 'Pressed':
        button.SetState(1)
        dvTLP.HidePopup("Windows Laptop Help popup")
    elif state == 'Released':
        button.SetState(0)
        

#Shutdown button
btn_shutdown = Button(dvTLP, 8)
@event(btn_shutdown, ButtonEventList)
def ShowShutdownPage(button, state):
    if state == 'Pressed':
        button.SetState(1)
        dvTLP.HideAllPopups()
        dvTLP.ShowPage("Shutdown confirmation")
    elif state == 'Released':
        button.SetState(0)

btn_shdnYes = Button(dvTLP, 6)
@event(btn_shdnYes, ButtonEventList)
def ShutdownYes(button, state):
    if state == 'Pressed':
        button.SetState(1)
    
        #lock drawer with control? 
        #turn off projector
        if dvPRJ.Update('Power') == 'On':
            dvPRJ.Set('Power', 'Off')
        
        #Set Audio levels back to defaults
        mic_val = -18
        lvl_mic.SetLevel(mic_val)
        
        prog_val = -18 
        lvl_prog.SetLevel(prog_val)

        #set Cynap as input
        dvScalar.Set('Input', '3', {'Type': 'Audio/Visual'})
        
        #switch to start page
        dvTLP.ShowPage("Start Page")
        
    elif state == 'Released':
        button.SetState(0)

btn_shdnNo = Button(dvTLP, 7)
@event(btn_shdnNo, 'Pressed')
def ShutdownNo(button, state):
    dvTLP.ShowPage("Main Page")


        
#Sleep timer
"""TODO The sleep timer seems to be related to a button press. I don't want to 
        sleep on a buton press I want an inactivity timeout. 
        
        When innactive for certain time - check page we're on. If it's the start page 
        then trigger sleep event. """

#change sleep state event 
"""TODO I don't know if this routine will work properly on a tap if it's off. 
        I think I still need a sleep timer which should go above here
@event(dvTLP, 'SleepChanged')
def HandleSleepChange(tlp, state):
    if state is 'Awake':
        tlp.Wake()
        tlp.ShowPage('Start Page')
    else:
        tlp.Sleep()
""" #Commented out for now
# Define UI Object Events

def Initialize():
    dvTLP.HideAllPopups()
    dvTLP.ShowPage('Start Page')
    

