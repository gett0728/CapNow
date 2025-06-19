import os
import sys
import json
import time
import threading
import msvcrt
from datetime import datetime

import tkinter as tk
from tkinter import filedialog, ttk
import keyboard
import pystray
from pystray import MenuItem as item
from PIL import ImageGrab, Image


CONFIG_FILE = "settings.json"

default_config = {
    "format": "png",
    "hotkey": "F3",
    "save_dir": "saved_images"
}