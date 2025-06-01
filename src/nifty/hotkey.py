from pynput import keyboard as pynput_keyboard
from threading import Thread

class HotkeyListener:
    def __init__(self, hotkey, callback):
        self.hotkey = hotkey
        self.callback = callback
        self.listener = None

    def start(self):
        def for_canonical(f):
            return lambda k: f(self.listener.canonical(k))

        hotkey = pynput_keyboard.HotKey(
            pynput_keyboard.HotKey.parse(self.hotkey),
            lambda: self.callback()
        )
        def on_press(key):
            hotkey.press(key)
        def on_release(key):
            hotkey.release(key)
        self.listener = pynput_keyboard.Listener(
            on_press=on_press,
            on_release=on_release
        )
        Thread(target=self.listener.run, daemon=True).start()

    def stop(self):
        if self.listener:
            self.listener.stop() 