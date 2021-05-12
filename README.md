
# yuruyuru_python

ESP32組み込み向けmicro pythonのサンプルコード群です！

# 手順

## 環境構築

ESP32用micropython バイナリ(esp32-idf3-20210202-v1.14.bin)をダウンロード   
[ダウンロードリンク](https://micropython.org/download/esp32/)

Silicon labのドライバをインストール    
[ダウンロードリンク](https://jp.silabs.com/developers/usb-to-uart-bridge-vcp-drivers)

### micro pythonのESP32への書き込み
#### Macの場合
```python
> pip install esptool
> esptool.py --port /dev/cu.SLAB_USBtoUART erase_flash
> esptool.py --chip esp32 --port /dev/cu.SLAB_USBtoUART write_flash -z 0x1000 esp32-idf3-20210202-v1.14.bin
```

#### Windowsの場合
```python
> esptool.py --port COM3 erase_flash
> esptool.py --chip esp32 --port COM3 write_flash -z 0x1000 esp32-idf3-20210202-v1.14.bin
```

## REPL(Read Evaluate Print Loop)

ESP32上でコマンドを実行できる対話型インタプリタ！

### REPLの立ち上げ
#### Macの場合    
```python
> screen /dev/tty.SLAB_USBtoUART 115200
```

#### Windowsの場合    
Teratermのダウンロード    
[ダウンロードリンク](https://forest.watch.impress.co.jp/library/software/utf8teraterm/)    
COMポートに接続    
設定->シリアルポート->スピードを115200に設定。(UARTのボーレート)    
USB抜き差し、切断再接続を繰り返して文字化けを解消    

### 動作確認
```python
> import os
> os.uname() # HW, FW情報の表示
> os.listdir() # ls
```

### GPIOを動かしてみる

```python
> import machine
> pin14 = machine.Pin(14, machine.Pin.OUT) # IN or OUT
> pin14.value(1) # High
```

これでIO14がHigh出力になる。

## プログラムの書き込み

```python
> pip install adafruit-ampy
> ampy -d 1 -p /dev/tty.SLAB_USBtoUART put main.py
```

Lチカで確認する。
