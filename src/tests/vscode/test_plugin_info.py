import os
import time

import pytest

from src.models.chrome import Chrome
from src.utils.general import read_file

DATA_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + "/data/"


@pytest.mark.vscode
def test_plugin_info(setup_vscode):
    # Automates Polarion MTA-511

    vscode = setup_vscode
    vscode.set_focus()
    fetched_vscode_plugin_info = vscode.get_plugin_text()
    expected_vscode_plugin_info = read_file(DATA_DIR + "vscode_plugin_info.txt").split("\n")
    vscode.close_active_tab()

    assert set(expected_vscode_plugin_info) == set(fetched_vscode_plugin_info)


@pytest.mark.vscode
def test_plugin_links(setup_vscode):
    # Automates Polarion MTA-512

    links = {
        "mta": "https://developers.redhat.com/products/mta/download",
        "extension": "https://marketplace.visualstudio.com/items?itemName=redhat.mta-vscode-extension",
        "eclipse che": "https://eclipse.dev/che/",
        "mit": "https://github.com/windup/rhamt-vscode-extension/blob/HEAD/LICENSE",
    }

    vscode = setup_vscode
    chrome = Chrome()
    vscode.set_focus()
    vscode.close_all_tabs()
    vscode.open_plugin_info(True)
    time.sleep(4)
    vscode.press_keys("tab")
    time.sleep(4)
    vscode.press_keys("tab")
    time.sleep(4)
    vscode.press_keys("enter")
    time.sleep(4)
    vscode.press_keys("enter")
    time.sleep(4)
    open_url = chrome.get_chrome_focused_tab_url()
    assert open_url == links["mta"]
    chrome.close_tab(open_url)

    vscode.set_focus()
    vscode.press_keys("tab")
    time.sleep(4)
    vscode.press_keys("enter")
    time.sleep(4)
    vscode.press_keys("enter")
    time.sleep(4)
    open_url = chrome.get_chrome_focused_tab_url()
    assert open_url == links["extension"]
    chrome.close_tab(open_url)

    vscode.set_focus()
    vscode.press_keys("tab")
    time.sleep(4)
    vscode.press_keys("enter")
    time.sleep(4)
    vscode.press_keys("enter")
    time.sleep(4)
    open_url = chrome.get_chrome_focused_tab_url()
    assert open_url == links["eclipse che"]
    chrome.close_tab(open_url)

    vscode.set_focus()
    vscode.press_keys("tab")
    time.sleep(4)
    vscode.press_keys("enter")
    time.sleep(4)
    vscode.press_keys("enter")
    time.sleep(4)
    open_url = chrome.get_chrome_focused_tab_url()
    assert open_url == links["mit"]
    chrome.close_tab(open_url)
