from _module import *

#設定読み込み
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
            for k, v in default_config.items():
                if k not in config:
                    config[k] = v
            return config
    else:
        save_config(default_config)
        return default_config


#設定保存
def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)


config = load_config()


#ファイル名の重複防止
def get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


#クリップボード上の画像を保存
def save_clipboard_image():
    image = ImageGrab.grabclipboard()

    if isinstance(image, Image.Image):
        os.makedirs(config["save_dir"], exist_ok=True)
        filename = f'{get_timestamp()}.{config["format"]}'
        path = os.path.join(config["save_dir"], filename)

        if config["format"] == "jpg":
            image = image.convert("RGB")
            image.save(path, "JPEG")
        else:
            image.save(path, config["format"].upper())


#ホットキーの監視
def start_hotkey_listener():
    try:
        keyboard.add_hotkey(config["hotkey"], save_clipboard_image)
    except:
        pass


#ホットキー変更
def change_hotkey(icon, item):
    def show_hotkey_dialog():
        pressed_keys = set()
        result = {"key_combo": None}

        def on_key_press(e):
            if e.event_type != "down":
                return
            pressed_keys.clear()
            if e.modifiers:
                pressed_keys.update(e.modifiers)
            pressed_keys.add(e.name)
            keys_sorted = sorted(pressed_keys, key=str.lower)
            text.set(" + ".join(k.capitalize() for k in keys_sorted))

        def on_ok():
            result["key_combo"] = text.get()
            root.quit()

        def on_cancel():
            result["key_combo"] = None
            root.quit()

        root = tk.Tk()
        root.title("保存するキーを設定")
        root.geometry("300x140")
        root.resizable(False, False)

        label = tk.Label(root, text="保存するキーを押してください", pady=10)
        label.pack()
        label = tk.Label(root, text=f'現在設定されているキー: {config["hotkey"]}')
        label.pack()

        text = tk.StringVar()

        entry = tk.Entry(root, textvariable=text, font=("Yu Gothic UI", 12), justify="center", state="readonly")
        entry.pack(pady=5, ipadx=10)

        frame = tk.Frame(root)
        frame.pack(pady=10)
        
        ok_btn = tk.Button(frame, text="OK", width=10, command=on_ok)
        cancel_btn = tk.Button(frame, text="Cancel", width=10, command=on_cancel)
        ok_btn.pack(side="left", padx=5)
        cancel_btn.pack(side="right", padx=5)

        keyboard.hook(on_key_press)
        root.mainloop()
        keyboard.unhook_all()
        root.destroy()

        return result["key_combo"]

    new_key = show_hotkey_dialog()

    if new_key:
        try:
            keyboard.remove_hotkey(config["hotkey"])
        except:
            pass

        config["hotkey"] = new_key
        save_config(config)

        try:
            keyboard.add_hotkey(new_key, save_clipboard_image)
        except:
            pass


#保存形式変更
def change_format(icon, item):
    def on_submit():
        selected = combo.get()

        if selected:
            config["format"] = selected
            save_config(config)

        win.destroy()

    formats = ["jpg", "png", "bmp", "gif"]
    win = tk.Tk()
    win.title("保存形式を選択")
    label = tk.Label(win, text="保存形式を選択してください")
    label.pack(padx=10, pady=10)
    combo = ttk.Combobox(win, values=formats, state="readonly")
    combo.set(config["format"])
    combo.pack(padx=10, pady=10)
    button = tk.Button(win, text="OK", command=on_submit)
    button.pack(pady=10)
    win.mainloop()


#保存フォルダの変更
def change_save_dir(icon, item):
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="保存フォルダを選択")

    if folder:
        config["save_dir"] = folder
        save_config(config)

    root.destroy()