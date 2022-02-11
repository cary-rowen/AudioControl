#-*- coding:utf-8 -*-
# AudioControl addon for NVDA
# Copyright 2021-2022 Cary-Rowen, Youlan, Cyrille Bougot, Chenfu
# released under GPL.

from ctypes import (
	Structure,
	c_char,
	c_ulong,
	POINTER,
	byref,
	cdll,
)

from scriptHandler import script
from synthDriverHandler import getSynth, setSynth
import ui
import config
import nvwave
import tones
import core
import os
import wx
import globalPluginHandler
import addonHandler

addonHandler.initTranslation()

path = os.path.dirname(__file__)
os.putenv('path', os.pathsep.join([os.getenv('path'), path]))


def friendlyName(text):
	name_Dict = {
		"WeChat": _("WeChat"),
		"taskhostw": _("System reminder"),
		"chrome": _("Google Chrome"),
		}

	text = text.decode('gb2312')
	text = text.split(".")[0]
	text = name_Dict.get(text, text)
	return text


dll = None
dll = cdll.LoadLibrary(os.path.join(path, 'AudioControl.dll'))

# Controls the current speaker by default
nType = 0

# Get session name and session ID
INFONAME = c_char * 128


class sessionInfo(Structure):
	_fields_ = [
	("id", c_ulong),
	("name", INFONAME)
	]


getProcessName = dll.getProcessName
getProcessName.argtypes = [POINTER(sessionInfo)]

confspec = {
"isAutoMyVolume": "integer(default=0)"
}
config.conf.spec["audioControl"] = confspec

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	nType = 0
	isAutoMyVolume = config.conf["audioControl"]["isAutoMyVolume"]
	scriptCategory = _("Audio control")

	def __init__(self):
		super().__init__()
		self.myVolume = dll.getVolume(1)
		if self.isAutoMyVolume == 1:
			self.setMyVolume()

	def setMyVolume(self):
		curVolume = dll.getVolume(1)
		if self.myVolume != curVolume:
			dll.setVolume(1, self.myVolume)
		if self.isAutoMyVolume == 1:
			wx.CallLater(500, self.setMyVolume)

	@script(
		description=_("Prohibit the microphone volume from being automatically adjusted by other programs"),
		gestures=["kb:Windows+control+alt+NumpadDelete", "kb(laptop):Windows+control+alt+."]
		)
	def script_autoSetMyVolume(self, gesture):
		self.isAutoMyVolume = (self.isAutoMyVolume+1)%2
		config.conf["audioControl"]["isAutoMyVolume"]=self.isAutoMyVolume
		if self.isAutoMyVolume == 0:
			ui.message(_("Default"))
		if self.isAutoMyVolume == 1:
			self.myVolume = dll.getVolume(1)
			self.setMyVolume()
			ui.message(_("Prevent automatic adjustment of microphone volume"))

	@script(
		description=_("Increase volume"),
		gestures=["kb:Windows+control+alt+Numpad8", "kb(laptop):Windows+control+alt+UpArrow"]
	)
	def script_volumeUp(self, gesture):
		if 0 == self.nType:
			self.vVolumeUp()
		elif 1 == self.nType:
			self.mVolumeUp()
		elif 2 == self.nType:
			self.sVolumeUp()

	def vVolumeUp(self):
		num = dll.getVolume(0)
		num = num + 1
		if dll.getMaxVol() >= num:
			dll.setVolume(0, num)
			ui.message(_("{} Increase master volume").format(num))
		else:
			ui.message(_("100 Maximum master volume"))

	def mVolumeUp(self):
		num = dll.getVolume(1)
		num = num + 1
		if dll.getMaxVol() >= num:
			dll.setVolume(1, num)
			self.myVolume = num
			str = _("{} Increase microphone volume").format(num)
			ui.message(str)
		else:
			ui.message(_("100 Maximum microphone volume"))

	def sVolumeUp(self):
		info = sessionInfo()
		info.id = dll.getNowSession()
		num = dll.getVolume(2, info.id)
		num = num + 1
		getProcessName(byref(info))
		if dll.getMaxVol() >= num:
			dll.setVolume(2, num, info.id)
			strs = "{}".format(num)
			ui.message(_("{} Increase {} volume").format(strs, friendlyName(info.name)))
		else:
			ui.message(_("100 maximum {} volume").format(friendlyName(info.name)))

	@script(
		description=_("Decrease the volume"),
		gestures=["kb:Windows+control+alt+Numpad2", "kb(laptop):Windows+control+alt+DownArrow"]
	)
	def script_volumeDown(self, gesture):
		if 0 == self.nType:
			self.vVolumeDown()
		elif 1 == self.nType:
			self.mVolumeDown()
		elif 2 == self.nType:
			self.sVolumeDown()

	def vVolumeDown(self):
		num = dll.getVolume(0)
		num = num - 1
		if dll.getMinVol() <= num:
			dll.setVolume(0, num)
			ui.message(_("{} Decrease master volume").format(num))
		else:
			ui.message(_("0 Minimum master volume"))

	def mVolumeDown(self):
		num = dll.getVolume(1)
		num = num - 1
		if dll.getMinVol() <= num:
			dll.setVolume(1, num)
			self.myVolume = num
			ui.message(_("{} Decrease microphone volume").format(num))
		else:
			ui.message(_("0 Minimum microphone volume"))

	def sVolumeDown(self):
		info = sessionInfo()
		info.id = dll.getNowSession()
		num = dll.getVolume(2, info.id)
		num = num - 1
		getProcessName(byref(info))
		if dll.getMinVol() <= num:
			dll.setVolume(2, num, info.id)
			strs = "{}".format(num)
			ui.message(_("{} Decrease {} volume").format(strs, friendlyName(info.name)))
		else:
			ui.message(_("0 lowest {} volume").format(friendlyName(info.name)))

	def mMute(self):
		dll.setMute(1, not dll.getMute(1))
		if dll.getMute(1):
			ui.message(_("microphone off"))
		else:
			ui.message(_("microphone on"))

	def vMute(self):
		dll.setMute(0, not dll.getMute(0))
		if dll.getMute(0):
			ui.message(_("Mute"))
		else:
			ui.message(_("Unmute"))

	def sMute(self):
		info = sessionInfo()
		info.id = dll.getNowSession()
		dll.setMute(2, not dll.getMute(2, info.id), info.id)
		if dll.getMute(2, info.id):
			strs = _("Closed")
		else:
			strs = _("Open")
		getProcessName(byref(info))
		ui.message(_("{} {} volume").format(strs, friendlyName(info.name)))


	@script(
		description=_("Switch to the previous application"),
		gestures=["kb:Windows+control+alt+Numpad4", "kb(laptop):Windows+control+alt+LeftArrow"]
	)
	def script_LastSession(self, gesture):
		sessionID = dll.getSessionID()
		if self.nType == 2 and sessionID == 0:
			if self.nType > 0:
				self.nType = self.nType - 1
				dll.setSessionID(-1)
		elif self.nType == 1:
			self.nType = 0

		if 0 == self.nType:
			status = _("Muted") if dll.getMute(0) == 1 else ""
			ui.message(status + _("Speaker volume {}").format(dll.getVolume(0)))
		elif 1 == self.nType:
			status = _("Microphone off") if dll.getMute(1) == 1 else ""
			ui.message(status + _("Microphone volume {}").format(dll.getVolume(1)))
		elif 2 == self.nType:
			info = sessionInfo()
			info.id = dll.getLastSession()
			getProcessName(byref(info))
			strs = _("{} volume {}").format(friendlyName(info.name), dll.getVolume(2, info.id))
			status = _("Muted") if dll.getMute(2, info.id) == 1 else ""
			ui.message(status + strs)

	@script(
		description=_("Switch to the next application"),
		gestures=["kb:Windows+Control+Alt+numpad6", "kb(laptop):Windows+Control+Alt+RightArrow"]
	)
	def script_NextSession(self, gesture):
		if self.nType < 2:
			self.nType = self.nType + 1

		if 0 == self.nType:
			status = _("Muted") if dll.getMute(0) == 1 else ""
			ui.message(status + _("Speaker volume {}").format(dll.getVolume(0)))
		elif 1 == self.nType:
			status = _("Microphone off") if dll.getMute(1)==1 else ""
			ui.message(status + _("Microphone volume {}").format(dll.getVolume(1)))
		elif 2 == self.nType:
			info = sessionInfo()
			info.id = dll.getNextSession()
			getProcessName(byref(info))
			strs = _("{} volume {}").format(friendlyName(info.name), dll.getVolume(2, info.id))
			status = _("Muted") if dll.getMute(2, info.id) == 1 else ""
			ui.message(status + strs)

	@script(
		description=_("Mute state switch"),
		gestures=["kb:Windows+control+alt+Numpad5", "kb(laptop):Windows+control+alt+m"]
	)
	def script_SetMute(self, gesture):
		if self.nType == 0:  # Speaker mute
			self.vMute()
		elif self.nType == 1:  # Microphone mute
			self.mMute()
		elif self.nType == 2:  # Session mute
			self.sMute()

	@script(
		description=_("Switch to the next audio output device"),
		gesture=("kb:NVDA+Windows+D")
	)
	def script_switchNextOutputDevice(self, gesture):
		self.switchOutputDevice(1)

	@script(
		description = _("Switch to the previous audio output device"),
		gesture=("kb:Shift+NVDA+Windows+D")
	)
	def script_switchPreviousOutputDevice(self, gesture):
		self.switchOutputDevice(-1)

	# Code borrowed from "NVDAScripts/" by Cyrille Bougot:
	# https://github.dev/CyrilleB79/NVDAScripts/blob/982bcce12e3b7e9377716f0bd43052e437a74832/globalPlugins/changeOutputDevice.py
	def switchOutputDevice(self, step):
		# Note: code mainly taken from NVDA gui/settingsDialogs.py (class SynthesizerSelectionDialog)
		deviceNames = nvwave.getOutputDeviceNames()
		# #11349: On Windows 10 20H1 and 20H2, Microsoft Sound Mapper returns an empty string.
		if deviceNames[0] in ("", "Microsoft Sound Mapper"):
			deviceNames[0] = _("Microsoft Sound Mapper")
		try:
			selection = deviceNames.index(config.conf["speech"]["outputDevice"])
		except ValueError:
			i = 0
		else:
			i = (selection + step) % len(deviceNames)

		audioDevice = deviceNames[i]
		config.conf["speech"]["outputDevice"] = audioDevice

		# Reinitialize the tones module and the synth to update the audio device
		# On the contrary to what is written in onOK method of SynthesizerSelectionDialog,
		# reinitializing only tones module is not enough.
		# Note: we need to reinitialize synth out of a script to avoid an error if the current synth is silence.
		def runOutOfScript():
			tones.terminate()
			setSynth(getSynth().name)
			tones.initialize()
			ui.message(audioDevice)
		core.callLater(0, runOutOfScript)
		return
