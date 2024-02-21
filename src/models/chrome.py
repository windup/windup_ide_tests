import subprocess
import time

from RPA.Desktop import Desktop

from src.utils.general import get_clipboard_text


class Chrome(Desktop):
    def __init__(self):
        super().__init__()

    def focus_tab(self, url):
        """
        Sets focus on a Chrome tab by its url, you don't need to provide the full URL, only a string that is unique in it
        """
        self.set_focus()
        time.sleep(1)
        self.press_keys("ctrl", "shift", "a")
        time.sleep(1)
        self.type_text(url)
        time.sleep(1)
        self.press_keys("enter")

    def get_chrome_focused_tab_url(self):
        """
        Returns the URL of the focused tab
        """
        self.set_focus()
        time.sleep(1)
        self.press_keys("ctrl", "l")
        time.sleep(1)
        self.press_keys("ctrl", "a")
        time.sleep(1)
        self.press_keys("ctrl", "c")
        return get_clipboard_text()

    def set_focus(self):
        """
        Sets chrome to be focused
        """
        subprocess.run(
            'wmctrl -a "Chrome"',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def close_tab(self, url: None):
        """
        Closes active tab
        """
        self.set_focus()
        if url:
            self.focus_tab(url)
        time.sleep(1)
        self.press_keys("ctrl", "w")
