# --------------------------------------------------- #
'''

Midi Remote control script for ableton Live, written by Chris Joseph


special credits to Alzy (Seppe?), his original script can be found at
https://forum.ableton.com/viewtopic.php?f=4&t=157266
Also thank you to
http://livecontrol.q3f.org/ableton-liveapi/articles/introduction-to-the-framework-classes/
and especially http://remotescripts.blogspot.ca/

Also credits to Julien Bayle for providing much of Ableton's API in an awesome
resource available at:
http://julienbayle.net/AbletonLiveRemoteScripts_Docs/_Framework/


'''


#.....................................
#---------------------------------------------------- #
from __future__ import with_statement

import sys
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import *
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.SessionComponent import SessionComponent
from _Framework.TransportComponent import TransportComponent
from _Framework.DeviceComponent import DeviceComponent
from _Framework.EncoderElement import EncoderElement
from _Framework.SessionZoomingComponent import SessionZoomingComponent

from _Framework.ChannelStripComponent import ChannelStripComponent
from _APC.DetailViewCntrlComponent import DetailViewCntrlComponent

from ._modules.ConfigurableButtonElement import ConfigurableButtonElement
from ._modules.DeviceNavComponent import DeviceNavComponent
from ._modules.TrackControllerComponent import TrackControllerComponent


from _Framework.MixerComponent import MixerComponent # Class encompassing several channel strips to form a mixer
from _Framework.SliderElement import SliderElement # Class representing a slider on the controller
from .consts import *


class CJ_controller(ControlSurface):
    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        self._device_selection_follows_track_selection = True
        with self.component_guard():
            self._suppress_send_midi = True
            self._suppress_session_highlight = True
            self._control_is_with_automap = False
            is_momentary = True
            self._suggested_input_port = ''
            self._suggested_output_port = ''
            self._setup_mixer_control()
            self._setup_session_control()
            self._setup_device_control()
            self._setup_transport_control()

    def _setup_session_control(self):
            # global session
            self.session = SessionComponent(GRIDSIZE[0],GRIDSIZE[1])

            self.session.name = 'Session_Control'
            self.matrix = ButtonMatrixElement()
            self.matrix.name = 'Button_Matrix'
            self.up_button = ButtonElement(True, MIDI_CC_TYPE, CHANNEL_MIXER, UP_BUTTON)
            self.down_button = ButtonElement(True, MIDI_CC_TYPE, CHANNEL_MIXER, DOWN_BUTTON)
            self.left_button = ButtonElement(True, MIDI_CC_TYPE, CHANNEL_MIXER, LEFT_BUTTON)
            self.right_button = ButtonElement(True, MIDI_CC_TYPE, CHANNEL_MIXER, RIGHT_BUTTON)

            self.session.set_scene_bank_buttons(self.down_button, self.up_button)
            self.session.set_track_bank_buttons(self.right_button, self.left_button)

            self.session_stop_buttons = []
            # scene_launch_buttons = []
            for row in range(GRIDSIZE[1]):
                button_row = []
                scene = self.session.scene(row)
                scene.name = 'Scene_' + str(row)
                # scene_launch_buttons.append(SCENE_BUTTONS[row])
                scene.set_launch_button(ButtonElement(True,MIDI_NOTE_TYPE,CHANNEL_MIXER, SCENE_BUTTONS[row]))
                scene.set_triggered_value(2)

                for column in range(GRIDSIZE[0]):
                    button = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, CHANNEL_MIXER, LAUNCH_BUTTONS[row][column])
                    button.name = str(column) + '_Clip_' + str(row) + '_Button'
                    button_row.append(button)
                    clip_slot = scene.clip_slot(column)
                    clip_slot.name = str(column) + '_Clip_Slot_' + str(row)
                    clip_slot.set_launch_button(button)

                self.matrix.add_row(tuple(button_row))

            for column in range(GRIDSIZE[0]):
                self.session_stop_buttons.append((ButtonElement(True, MIDI_NOTE_TYPE, CHANNEL_MIXER, TRACK_STOPS[column])))

            self._suppress_session_highlight = False
            self._suppress_send_midi = False
            self.set_highlighting_session_component(self.session)
            self.session.set_stop_track_clip_buttons(tuple(self.session_stop_buttons))
            self.session.set_mixer(self.mixer)





    def _set_session_highlight(self, track_offset, scene_offset, width, height, include_return_tracks):
        if not self._suppress_session_highlight:
            ControlSurface._set_session_highlight(self, track_offset, scene_offset, width, height, include_return_tracks)


    def _setup_mixer_control(self):
        num_tracks = GRIDSIZE[0] 
        self.mixer = MixerComponent(num_tracks)
        self.mixer.set_track_offset(0)
        self.song().view.selected_track = self.mixer.channel_strip(0)._track
        self.master = self.mixer.master_strip()
        self.master.set_volume_control(SliderElement(MIDI_CC_TYPE, CHANNEL_USER, MASTER_VOLUME))
        self.mixer.set_prehear_volume_control(SliderElement(MIDI_CC_TYPE, CHANNEL_USER, PREHEAR))

        for index in range(GRIDSIZE[0]):
            self.mixer.channel_strip(index).set_volume_control(SliderElement(MIDI_CC_TYPE, CHANNEL_MIXER, MIX_FADERS[index]))
            self.mixer.channel_strip(index).set_pan_control(SliderElement(MIDI_CC_TYPE, CHANNEL_MIXER, PAN_CONTROLS[index]))
            self.mixer.channel_strip(index).set_arm_button(ButtonElement(True, MIDI_CC_TYPE, CHANNEL_INST, ARM_BUTTONS[index])) #sets the record arm button
            self.mixer.channel_strip(index).set_solo_button(ButtonElement(True, MIDI_CC_TYPE, CHANNEL_INST, SOLO_BUTTONS[index]))
            self.mixer.channel_strip(index).set_mute_button(ButtonElement(True, MIDI_CC_TYPE, CHANNEL_INST, MUTE_BUTTONS[index]))
            self.mixer.channel_strip(index).set_select_button(ButtonElement(True, MIDI_CC_TYPE, CHANNEL_INST, TRACK_SELECTS[index]))
            self.mixer.channel_strip(index).set_send_controls([SliderElement(MIDI_CC_TYPE, CHANNEL_MIXER, SEND_CONTROLS[index][0]),
                                                              SliderElement(MIDI_CC_TYPE, CHANNEL_MIXER, SEND_CONTROLS[index][1]),
                                                              SliderElement(MIDI_CC_TYPE, CHANNEL_MIXER, SEND_CONTROLS[index][2]),
                                                              SliderElement(MIDI_CC_TYPE, CHANNEL_MIXER, SEND_CONTROLS[index][3])])

    def _setup_transport_control(self):
        self.stop_button = ButtonElement(False, MIDI_CC_TYPE, CHANNEL_MIXER, STOP_BUTTON)
        self.play_button = ButtonElement(False, MIDI_CC_TYPE, CHANNEL_MIXER, PLAY_BUTTON)
        self.record_button = ButtonElement(False,MIDI_CC_TYPE,CHANNEL_MIXER,RECORD_BUTTON)
        self.overdub_button = ButtonElement(False,MIDI_CC_TYPE,CHANNEL_MIXER,OVERDUB_BUTTON)
        self.transport = TransportComponent()
        self.transport.TEMPO_TOP = 188
        self.transport.set_stop_button(self.stop_button)
        self.transport.set_play_button(self.play_button)
        self.transport.set_overdub_button(self.overdub_button)
        self.transport.set_record_button(self.record_button)
        self.transport.set_seek_buttons(ButtonElement(False,MIDI_CC_TYPE,0,SEEK_LEFT), ButtonElement(False,MIDI_CC_TYPE,0,SEEK_RIGHT))
        self.transport.set_tempo_control(SliderElement(MIDI_CC_TYPE, CHANNEL_USER, TEMPO))
        self.transport.set_metronome_button(ButtonElement(False,MIDI_CC_TYPE,CHANNEL_USER, METRONOME))
        self.transport.set_tap_tempo_button(ButtonElement(False,MIDI_CC_TYPE,CHANNEL_USER,TAP_TEMPO))


    def _setup_device_control(self):
        is_momentary = True
        self._device = DeviceComponent()
        self._channelstrip = ChannelStripComponent()
        self._device.name = 'Device_Component'

        device_param_controls = []
        for index in range(8):
            device_param_controls.append(SliderElement(MIDI_CC_TYPE, CHANNEL_FX, MACRO_CONTROLS[index]))
        self._device.set_parameter_controls(device_param_controls)
        self._device.set_on_off_button(ButtonElement(True, MIDI_CC_TYPE, CHANNEL_FX, DEVICE_ON))
        self._device.set_lock_button(ButtonElement(True, MIDI_CC_TYPE, CHANNEL_FX, DEVICE_LOCK))
        self.up_bank_button = ButtonElement(True, MIDI_CC_TYPE, CHANNEL_FX, DEVICE_BANK_UP)
        self.down_bank_button = ButtonElement(True, MIDI_CC_TYPE, CHANNEL_FX, DEVICE_BANK_DOWN)
        self.set_device_component(self._device)
        self._device_nav = DeviceNavComponent()
        self._device_nav.set_device_nav_buttons(ButtonElement(True, MIDI_CC_TYPE, CHANNEL_FX, PREVIOUS_DEVICE),ButtonElement(True, MIDI_CC_TYPE, CHANNEL_FX, NEXT_DEVICE))
        self._device.set_bank_prev_button(self.down_bank_button)
        self._device.set_bank_next_button(self.up_bank_button)



    def disconnect(self):
        ControlSurface.disconnect(self)
        return None
