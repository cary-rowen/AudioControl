#-*- coding:utf-8 -*-
import config
import nvwave
import synthDriverHandler
import ui

def switchOutputDevice(step):
	names = nvwave.getOutputDeviceNames()
	try:
		selection = names.index(config.conf["speech"]["outputDevice"])
	except ValueError:
		i = 0
	else:
		i = (selection + step) % len(names)  # Always cycle

	config.conf["speech"]["outputDevice"] = names[i]
	synthDriverHandler.setSynth(synthDriverHandler.getSynth().name)  # 必须重新初始化合成器才能生效

	name = config.conf["speech"]["outputDevice"]
	name = name if name else _("Default device")
	ui.message(name)

