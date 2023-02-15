pytest_plugins = ["src.infra.fixtures.ide_fixture"]


# def pytest_generate_tests(metafunc):
#     if "configuration_name" in metafunc.fixturenames:
#         metafunc.parametrize("configuration_name", ["from parameters", "from parameters 1"])
#
#     if "target" in metafunc.fixturenames:
#         metafunc.parametrize("target", ["eap7", "openjdk17"])
#
#     if "source" in metafunc.fixturenames:
#         metafunc.parametrize("source", ["eap5", "openjdk11"])
