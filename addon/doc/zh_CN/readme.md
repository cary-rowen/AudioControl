## AudioControl-1.4.5（音频控制插件）

为正在运行的应用程序调整音量，设置静音状态以及切换NVDA声音输出的插件。

## 说明

**下表为默认热键方案，如果需要，您可以在NVDA“输入手势”对话框的“音频控制”类别下自行更改**

| 名称 | 台式机 | 笔记本 |
| ---- | ---- | ---- |
| 下一个声音输出设备 | NVDA+Windows+D | NVDA+Windows+D |
| 上一个声音输出设备 | Shift+NVDA+Windows+D | NVDA+Windows+D |
| 上一个应用程序/设备 | Windows+Control+Alt+小键盘4 | Windows+Control+Alt+Left |
| 下一个应用程序/设备 | Windows+Control+Alt+小键盘6 | Windows+Control+Alt+Right |
| 增大当前应用程序/设备的音量 | Windows+Control+Alt+小键盘8 | Windows+Control+Alt+Up |
| 减小当前应用程序/设备的音量 | Windows+Control+Alt+小键盘2 | Windows+Control+Alt+Down |
| 为当前选中应用程序/设备设置或取消静音状态 | Windows+Control+Alt+小键盘5 | Windows+Control+Alt+M |
| 锁定/解锁麦克风音量（防止其他应用自动调节麦克风音量） | Windows+Control+Alt+小键盘删除 | Windows+Control+Alt+句号 |

## 维护者

* Cary-Rowen （插件维护者）
* 幽兰少云（音频控制模块）；
* Cyrille Bougot (输出设备切换)
* 沉浮 （其他支持）

## 兼容性
**NVDA2019.3及最新**

## 1.7 版更新日志
1. 添加切换上一个音频输出设备的快捷键： Shift+NVDA+Windows+D;
2. 更安全更优雅的运行库调用方式，感谢好奇的 01 提供思路。

## 1.6 版更新日志
1. 修复一处自动安装运行库失败的错误；
2. 声音输出设备切换更加稳定，解决 tones.beep 不跟随切换的问题；
3. 声音输出改为循环切换模式 NVDA + Windows +D。

## 1.5版更新日志
1. 初步整理代码；
2. 添加了多语言支持；
3. 已经无需单独安装运行库；
4. 兼容 NVDA2021.1。

## 1.4.5版更新日志
1. 增加锁定/解锁麦克风音量功能，防止其他应用自动调节麦克风音量，如： 微信。
  - 由沉浮老师提供支持
2. 增加笔记本键盘方案，详见帮助文档。

## 1.4.2版更新日志
1. 切换设备/应用程序时可以读出其静音状态；
2. 切换到的应用程序不再包含扩展名（*.exe）。
3. 完善帮助文档。

## 1.4版更新日志
1. 增加切换 NVDA 输出设备的功能；
2. 支持自定义快捷键；
