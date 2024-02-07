import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--record-video",
        action="store_true",
        help="This options enables the record video fixture to record the test run.",
    )


def pytest_configure(config):
    pytest.record_video = config.getoption("--record-video")
