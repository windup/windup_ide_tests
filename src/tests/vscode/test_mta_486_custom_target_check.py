import pytest

APP_NAME = "custom target check"


@pytest.mark.parametrize("app_name", [APP_NAME])
@pytest.mark.parametrize(
    "analysis_data",
    [
        {
            APP_NAME: {"options": {"target": ["custom_target", "custom_target_1"]}},
        },
    ],
)
@pytest.mark.parametrize("ide", ["vscode"])
@pytest.mark.vscode
def test_mta_486_custom_target_check(setup_vscode, configurations, app_name, analysis_data, ide):
    # Automates Polarion MTA-486

    vscode = setup_vscode

    configuration_object, _, _ = configurations

    targets_list = configuration_object.configurations[0].options.target

    vscode.set_focus()
    vscode.run_simple_analysis(app_name)
    vscode.cancel_analysis()

    command_map = vscode.fetch_executed_cli_command_map()
    command_target = command_map["target"]

    assert set(command_target) == set(targets_list), f"Error: the following targets were not picked by the IDE: {','.join([tgt for tgt in targets_list if tgt not in command_target])}"
