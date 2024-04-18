import pytest

APP_NAME = "cli parameters check"


@pytest.mark.parametrize("app_name", [APP_NAME])
@pytest.mark.parametrize(
    "analysis_data",
    [
        {
            APP_NAME: {"options": {"target": ["eap", "eap7", "jakarta-ee"], "source": ["amazon", "apicurio"], "analyze-known-libraries": True, "overwrite": True}},
        },
    ],
)
@pytest.mark.parametrize("ide", ["vscode"])
@pytest.mark.vscode
def test_mta_493_generated_cli_paramters(setup_vscode, configurations, app_name, analysis_data, ide):
    # Automates Polarion MTA-493

    vscode = setup_vscode

    configuration_object, _, _ = configurations

    vscode.set_focus()
    vscode.run_simple_analysis(app_name)
    vscode.cancel_analysis()
    command_map = vscode.fetch_executed_cli_command_map()

    targets_list = configuration_object.configurations[0].options.target
    command_target = command_map["target"]
    assert set(command_target) == set(targets_list), f"Error: the following targets were not picked by the IDE: {','.join([tgt for tgt in targets_list if tgt not in command_target])}"

    sources_list = configuration_object.configurations[0].options.source
    command_source = command_map["source"]
    assert set(command_source) == set(sources_list), f"Error: the following sources were not picked by the IDE: {','.join([tgt for tgt in sources_list if tgt not in command_source])}"

    assert command_map["mode"] == "source-only"
    assert "overwrite" in command_map["advanced_options"]
    assert "analyze-known-libraries" in command_map["advanced_options"]
