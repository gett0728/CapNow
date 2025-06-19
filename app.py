from _main import *


#.exeが参照するリソースのパスを取得
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path) 
    
    return os.path.join(os.path.abspath("."), relative_path)


#起動時の重複チェック
def check_running():
    lock_path = os.path.join(os.environ.get("TEMP", "."), LOCK_FILE)

    try:
        lock_file = open(lock_path, "w")
        msvcrt.locking(lock_file.fileno(), msvcrt.LK_NBLCK, 1)
        return lock_file
    except:
        return None
    


#ポップアップメニュー
def setup_tray():
    icon_path = resource_path("images/icon.png")
    image = Image.open(icon_path)
    menu = (
        item("保存形式を変更", change_format),
        item("ホットキーを変更", change_hotkey),
        item("保存先フォルダを選択", change_save_dir),
        item("終了", quit)
    )
    icon = pystray.Icon("CapNow", image, "CapNow", menu)
    threading.Thread(target=icon.run, daemon=True).start()


def quit(icon, item):
    icon.stop()

    if "lock" in globals() and lock:
        try:
            lock.close()
            os.remove(os.path.join(os.environ.get("TEMP", "."), LOCK_FILE))
        except:
            pass
        

    os._exit(0)


LOCK_FILE = "app.lock"

if __name__ == "__main__":
    global lock
    lock = check_running()

    if not lock:
        sys.exit(0)

    setup_tray()
    start_hotkey_listener()

    try:
        while True:
            time.sleep(1)
    except:
        sys.exit(0)