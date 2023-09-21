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
        "--ide",
        action="store",
        help="This options to specify the IDE that will be tested",
    )


def pytest_configure(config):
    pytest.mtr = config.getoption("--mtr")
    pytest.mta = config.getoption("--mta")
    pytest.ide = config.getoption("--ide")
