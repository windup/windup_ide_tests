import os
import subprocess
from datetime import datetime

import pytest

from src.utils.general import get_screen_size

RECORD_DIR = (
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/archived_artifacts/videos"
)


@pytest.fixture(autouse=True)
def record_test_run(ide, frame_rate=24):

    if not pytest.record_video:
        return

    screen_size = get_screen_size()

    run_time = datetime.now().strftime("%d-%m-%Y_%H:%M")
    output_file = f"{RECORD_DIR}/{ide}_{run_time}.mp4"
    cmd = (
        f"ffmpeg -video_size {screen_size} -framerate {frame_rate} -f x11grab -i :0.0 {output_file}"
    )
    print("Executing command: " + cmd)
    p = subprocess.Popen(cmd, shell=True)

    yield

    # Stop the recording
    p.terminate()
    # Ensure the process has terminated before exiting
    p.wait()
