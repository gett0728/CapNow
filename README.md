# CapNow

CapNow は、**クリップボード上の画像をワンボタンで保存できる**シンプルなWindowsアプリです。  
起動後はタスクトレイに常駐し、最小限の操作でスクリーンショットの保存が可能になります。
<br><br>

## 動作環境
OS: Windows 10/11

Python: 3.12

PyInstaller: 6.13.0
<br><br>

## 使い方

### ① ビルド

CapNowはPythonで記述されているため、まず `.exe` にビルドする必要があります。

以下のコマンドでPyInstallerをインストールします：

```bash
pip install pyinstaller
```

以下のコマンドで`app.py`をビルドします。

```bash
pyinstaller app.py --add-data "images/icon.png;images" -w
```
※上記は一例なので、他のオプションでも構いません。
<br><br>

### ② 実行と操作

ビルド後に生成される`dist`フォルダの`app.exe`から起動してください。

起動後、画面右下のタスクトレイにアイコンが表示されるので、右クリックしてメニューを開いて諸々設定してください。

デフォルトでは、保存キーが`F3`、保存フォーマットが`png`となっています。

保存フォルダについては、同ディレクトリに`saved_images`が生成され、そこに保存されます。
