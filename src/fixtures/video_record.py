import os
import subprocess
from datetime import datetime

import pytest

from src.utils.general import get_screen_size

RECORD_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/archived_artifacts/videos"


@pytest.fixture(autouse=True)
def record_test_run(frame_rate=24):
    p = None

    if pytest.record_video:
        ide = "intellij" if pytest.intellij else "vscode"

        screen_size = get_screen_size()

        run_time = datetime.now().strftime("%d-%m-%Y_%H:%M")
        output_file = f"{RECORD_DIR}/{ide}_{run_time}.mp4"
        cmd = f"ffmpeg -video_size {screen_size} -framerate " f"{frame_rate} -f x11grab -i :0.0 {output_file}"
        print("Executing command: " + cmd)
        p = subprocess.Popen(cmd, shell=True)

    yield p
    if p:
        # Stop the recording
        p.terminate()
        # Ensure the process has terminated before exiting
        p.wait()
