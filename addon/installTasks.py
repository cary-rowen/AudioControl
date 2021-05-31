import wx
import gui
import ctypes
import os

def is_admin():
	try:
		return ctypes.windll.shell32.IsUserAnAdmin()
	except:
		return False

path = os.path.dirname(__file__)
RTPath = os.environ['WINDIR'] + R'\\sysWOW64\\'
if not os.path.isdir(RTPath):
	RTPath = os.environ['WINDIR'] + '\\system32\\'
RTvcp = 'msvcp120.dll'
RTvcr = 'msvcr120.dll'

def onInstall():
	if not(os.path.isfile(RTPath + RTvcp) or os.path.isfile(RTPath + RTvcr)):
		if not is_admin():
			gui.messageBox("在本插件安装后需要您授权管理员权限以安装相关运行库。", "温馨提示", wx.OK)
