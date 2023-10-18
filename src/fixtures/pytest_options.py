import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--mtr",
        action="store_true",
        help="This is when running a test case on MTR (Migration Toolkit for Runtime) plugin.",
    )
    parser.addoption(
        "--mta",
        action="store_true",
        help="This is when running a test case on MTA (Migration Toolkit for Application) plugin.",
    )
    parser.addoption(
        "--record-video",
        action="store_true",
        help="This options enables the record video fixture to record the test run.",
    )


def pytest_configure(config):
    pytest.mtr = config.getoption("--mtr")
    pytest.mta = config.getoption("--mta")
    pytest.record_video = config.getoption("--record-video")
