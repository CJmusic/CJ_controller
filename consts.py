#Christopher Zaworski, 2017

'''
This file is for setting what midi controls to use for each feature
with the control script. Currently this is the setup I use for my Akai
MPD 26.

It can easily be adapted to use with other MIDI controllers:

I recommended that you download a program to monitor incoming midi messages,
such as MIDI Monitor for OS X, so that you can know what MIDI messages your
controller is sending and then simply change the values here to correspond
to the midi note and CC number you want to assign to each control.
'''

CHANNEL = 4 #I have this set to midi channel 2 (which corresponds to 1
    #in python since python counts from zero) on my MPD, that way
    #I have all midi 128 notes available to me on channel 1 (0 in python)
    #for playing instruments
CHANNEL_USER = 0
CHANNEL_FX = 1
CHANNEL_INST = 2
CHANNEL_MIXER = 3

##RED BOX Control
GRIDSIZE = [8,1] ##the red box grid size(does not have to be square)

LAUNCH_BUTTONS =[[51,52,53,54,55,56,57,58,59]]
    ##these are the midi note values that correspond to the scene launch
    #buttons withing the SessionGrid. You will need to add more values or
    #delete values coressponding to the size of the Grid you set.

SCENE_BUTTONS = [72]#,73,74,75]

##NAV Controls, move the red box in live
DOWN_BUTTON =111
UP_BUTTON = 112
LEFT_BUTTON =113
RIGHT_BUTTON = 114


##MIXER Controls
#The below mixer controls correspond to the RedBox in Live. Again, if you
#change the grid size you will need to update these lists accordingly.


MUTE_BUTTONS = [57,58,59,60,61,62,63,64]
ARM_BUTTONS =  [65,66,67,68,69,70,71,72]
SOLO_BUTTONS = [81,82,83,84,85,86,87,88]

MIX_FADERS =   [12,13,14,15,16,17,18,19] ##these correspond to the CC message number for each fader
PAN_CONTROLS = [20,21,22,23,24,25,26,27]

SEND_CONTROLS = [[28,36,44,52],
                    [29,37,45,53],
                    [30,38,46,54],
                    [31,39,47,55],
                    [32,40,48,56],
                    [33,41,49,57],
                    [34,42,50,58],
                    [35,43,51,59]]


MASTER_VOLUME = 0
PREHEAR = 1
TEMPO = 2
TAP_TEMPO = 10
METRONOME = 11



TRACK_SELECTS = [73,74,75,76,77,78,79,80]
TRACK_STOPS =   [43,44,45,46,47,48,49,50]

##DEVICE Controls
#use these in combination with the track select buttons to quickly navigate to
#and control devices

NEXT_DEVICE = 77
PREVIOUS_DEVICE = 76

DEVICE_ON = 79
DEVICE_LOCK = 78 #Locks your macro controls to current device regardless of where
     #you are in your session
DEVICE_BANK_UP = 81
DEVICE_BANK_DOWN = 80


#MACRO Controls
#these correspond to the knobs and Sliders you want to use to for the first 8
#controls in any ableton device (these also correspond to the 8 macro knobs in
#an instrument or effects rack)


MACRO_CONTROLS = [0,1,2,3,4,5,6,7]

#TRANSPORT Controls
#channels may be different from the channel you specify above

PLAY_BUTTON = 118
STOP_BUTTON = 117
RECORD_BUTTON = 119
OVERDUB_BUTTON = 120
SEEK_LEFT = 116
SEEK_RIGHT = 115
