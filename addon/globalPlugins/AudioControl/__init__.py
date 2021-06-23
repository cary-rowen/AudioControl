#-*- coding:utf-8 -*-

from ctypes import (
	Structure,
	c_char,
	c_ulong,
	POINTER,
	byref,
	cdll,
	windll
)

from . switchOutputDevice import *

from scriptHandler import script

import ui
import os
import sys
import wx
import globalPluginHandler
import addonHandler
import shutil

addonHandler.initTranslation()

path = os.path.dirname(__file__)
RTPath = os.environ['WINDIR'] + R'\\sysWOW64\\'
if not os.path.isdir(RTPath):
	RTPath = os.environ['WINDIR'] + '\\system32\\'
RTvcp = 'msvcp120.dll'
RTvcr = 'msvcr120.dll'

def is_admin():
	try:
		return windll.shell32.IsUserAnAdmin()
	except:
		return False

if not(os.path.isfile(RTPath + RTvcp) or os.path.isfile(RTPath + RTvcr)):
	if is_admin():
		if not os.path.isfile(RTPath + RTvcp): shutil.copy(os.path.join(path, RTvcp), RTPath)
		if not os.path.isfile(RTPath + RTvcr): shutil.copy(os.path.join(path, RTvcr), RTPath)
	else:
		if sys.version_info[0] == 3: windll.shell32.ShellExecuteW(None, 'runas', sys.executable, __file__, None, 1)

def friendlyName(text):
	name_Dict={
	"WeChat":_("WeChat"),
	"taskhostw":_("System reminder"),
	"chrome":_("Google Chrome"),
}
	text = text.decode('gb2312')
	text = text.split(".")[0]
	text=name_Dict.get(text, text)
	return text

dll = None
dll = cdll.LoadLibrary(os.path.join(path, 'AudioControlDll.dll'))

#为了记录当前控制的是什么设备,默认为控制扬声器
nType=0

#准备一些结构体需要的数据，为了获取绘画名称等信息
INFONAME = c_char * 128

class sessionInfo(Structure):
	_fields_ = [
		("id",c_ulong),
		("name", INFONAME)
]

getProcessName = dll.getProcessName
getProcessName.argtypes = [POINTER(sessionInfo)]

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
 nType = 0
 isAutoMyVolume=0
 scriptCategory=_("Audio control")

 def __init__(self):
  super().__init__()
  self.myVolume=dll.getVolume(1)
  if self.isAutoMyVolume==1:
   self.setMyVolume()

 def setMyVolume(self):
  curVolume=dll.getVolume(1)
  if self.myVolume!=curVolume:
   dll.setVolume(1,self.myVolume)
  if self.isAutoMyVolume==1:
   wx.CallLater(500,self.setMyVolume)

 @script(
  description=_("Prohibit the microphone volume from being automatically adjusted by other programs"),
  gestures=["kb:Windows+control+alt+NumpadDelete", "kb(laptop):Windows+control+alt+."]
 )
 def script_autoSetMyVolume(self, gesture):
  self.isAutoMyVolume=(self.isAutoMyVolume+1)%2
  if self.isAutoMyVolume==0:
   ui.message(_("Default"))
  if self.isAutoMyVolume==1:
   self.myVolume=dll.getVolume(1)
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
  num=num+1
  if dll.getMaxVol() >= num:
   dll.setVolume(0, num)
   ui.message(_("{} Increase master volume").format(num))
  else:
   ui.message(_("100 Maximum master volume"))

 def mVolumeUp(self):
  num = dll.getVolume(1)
  num=num+1
  if dll.getMaxVol() >= num:
   dll.setVolume(1, num)
   self.myVolume=num
   str = _("{} Increase microphone volume").format(num)
   ui.message(str)
  else:
   ui.message(_("100 Maximum microphone volume"))

 def sVolumeUp(self):
  info = sessionInfo()
  info.id = dll.getNowSession()
  num = dll.getVolume(2, info.id)
  num=num+1
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
  num=num-1
  if dll.getMinVol() <= num:
   dll.setVolume(0, num)
   ui.message(_("{} Decrease master volume").format(num))
  else:
   ui.message(_("0 Minimum master volume"))

 def mVolumeDown(self):
  num = dll.getVolume(1)
  num=num-1
  if dll.getMinVol() <= num:
   dll.setVolume(1, num)
   self.myVolume=num
   ui.message(_("{} Decrease microphone volume").format(num))
  else:
   ui.message(_("0 Minimum microphone volume"))

 def sVolumeDown(self):
  info = sessionInfo()
  info.id = dll.getNowSession()
  num = dll.getVolume(2, info.id)
  num=num-1
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
    self.nType=self.nType-1
    dll.setSessionID(-1)
  elif self.nType == 1:
   self.nType = 0

  if 0 == self.nType:
   status = _("Muted") if dll.getMute(0)==1 else ""
   ui.message(status + _("Speaker volume {}").format(dll.getVolume(0)))
  elif 1 == self.nType:
   status = _("Microphone off") if dll.getMute(1)==1 else ""
   ui.message(status+_("Microphone volume {}").format(dll.getVolume(1)))
  elif 2 == self.nType:
   info = sessionInfo()
   info.id = dll.getLastSession()
   getProcessName(byref(info))
   strs = _("{} volume {}").format(friendlyName(info.name), dll.getVolume(2, info.id))
   status = _("Muted") if dll.getMute(2, info.id)==1 else ""
   ui.message(status+strs)

 @script(
  description=_("Switch to the next application"),
  gestures=["kb:Windows+Control+Alt+numpad6", "kb(laptop):Windows+Control+Alt+RightArrow"]
 )
 def script_NextSession(self, gesture):
  if self.nType < 2:
   self.nType = self.nType+1

  if 0 == self.nType:
   status = _("Muted") if dll.getMute(0)==1 else ""
   ui.message(status+_("Speaker volume {}").format(dll.getVolume(0)))
  elif 1 == self.nType:
   status = _("Microphone off") if dll.getMute(1)==1 else ""
   ui.message(status + _("Microphone volume {}").format(dll.getVolume(1)))
  elif 2 == self.nType:
   info = sessionInfo()
   info.id = dll.getNextSession()
   getProcessName(byref(info))
   strs = _("{} volume {}").format(friendlyName(info.name), dll.getVolume(2, info.id))
   status = _("Muted") if dll.getMute(2, info.id)==1 else ""
   ui.message(status+strs)

 @script(
  description=_("Mute state switch"),
  gestures=["kb:Windows+control+alt+Numpad5", "kb(laptop):Windows+control+alt+m"]
 )
 def script_SetMute(self, gesture):
  if self.nType == 0:#扬声器静音
   self.vMute()
  elif self.nType == 1:#麦克风静音
   self.mMute()
  elif self.nType == 2:#绘画静音
   self.sMute()

 @script(
  description=_("Switch to the next audio output device"),
  gestures=["kb:Windows+Control+Alt+numpad9", "kb(laptop):Windows+Control+Alt+PageDown"]
 )
 def script_switchNextOutputDevice(self, gesture):
  switchOutputDevice(1)

 @script(
  description=_("Switch to the previous audio output device"),
  gestures=["kb:Windows+Control+Alt+numpad7", "kb(laptop):Windows+Control+Alt+PageUp"]
 )
 def script_switchPreviousOutputDevice(self, gesture):
  switchOutputDevice(-1)
