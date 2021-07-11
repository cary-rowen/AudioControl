# AudioControl-1.5（音訊控制附加元件）

為正在運行的應用程式調整音量，設置靜音狀態以及切換NVDA聲音輸出的附加元件。

## 說明

**下表為預設熱鍵方案，如果需要，您可以在NVDA“輸入手勢”對話方塊的“音訊控制”類別下自行更改**

| 名稱 | 桌上型電腦 | 筆記型電腦 |
| ---- | ---- | ---- |
| 將 NVDA 切換到上一個聲音輸出裝置 | Windows+Control+Alt+數字鍵盤7 | Windows+Control+Alt+PageUp |
| 將 NVDA 切換到下一個聲音輸出裝置 | Windows+Control+Alt+數字鍵盤9 | Windows+Control+Alt+PageDown |
| 上一個應用程式/裝置 | Windows+Control+Alt+數字鍵盤4 | Windows+Control+Alt+Left |
| 下一個應用程式/裝置 | Windows+Control+Alt+數字鍵盤6 | Windows+Control+Alt+Right |
| 提高當前應用程式/裝置的音量 | Windows+Control+Alt+數字鍵盤8 | Windows+Control+Alt+Up |
| 降低當前應用程式/裝置的音量 | Windows+Control+Alt+數字鍵盤2 | Windows+Control+Alt+Down |
| 為當前選中應用程式/裝置設置或取消靜音狀態 | Windows+Control+Alt+數字鍵盤5 | Windows+Control+Alt+M |
| 鎖定/解鎖麥克風音量（防止其他程式自動調整麥克風音量） | Windows+Control+Alt+數字鍵盤刪除 | Windows+Control+Alt+句號 |

## 維護者

* Cary-Rowen （附加元件維護）
* 幽蘭少雲（音訊控制模組）；
* 好奇的01（聲音輸出切換模組）；
* 沉浮 （其他支持）

## 相容性
**NVDA2019.3及最新**

## 1.5版更新日誌
1. 初步整理代碼；
2. 添加了多語言支援；
3. 已經無需單獨安裝運行庫；
4. 相容 NVDA2021.1。

## 1.4.5版更新日誌
1. 增加鎖定/解鎖麥克風音量功能，防止其他應用自動調節麥克風音量，如： 微信。
  - 由沉浮老師提供支援
2. 增加筆記本鍵盤方案，詳見説明文檔。

## 1.4.2版更新日誌
1. 切換裝置/應用程式時可以讀出其靜音狀態；
2. 切換到的應用程式不再包含副檔名（*.exe）。
3. 完善幫助文檔。

## 1.4版更新日誌
1. 增加切換 NVDA 輸出裝置的功能；
2. 支持自訂快速鍵；
