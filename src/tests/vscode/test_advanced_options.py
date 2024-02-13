import pytest

CONF_JSON = [
    {
        "overwrite analysis": {"options": {"target": ["eap8"]}},
    },
]


@pytest.mark.parametrize("app_name", ["overwrite analysis"])
@pytest.mark.parametrize("analysis_data", CONF_JSON)
@pytest.mark.parametrize("ide", ["vscode"])
@pytest.mark.vscode
def test_overwrite_option(setup_vscode, vscode_config, configurations, app_name, analysis_data, ide):
    # Automates polarion MTA-481
    vscode = setup_vscode
    vscode.set_focus()

    vscode.run_simple_analysis(app_name)
    assert vscode.is_analysis_complete()

    configurations_object, _, _ = configurations
    running_configuration = configurations_object.configurations[0]
    running_configuration.options.overwrite = True

    model_json_path = f"{vscode_config['plugin_cache_path']}/model.json"
    vscode.update_configuration(model_json_path, running_configuration)

    vscode.clear_terminal_output_panel()
    vscode.run_simple_analysis(app_name)
    assert vscode.is_analysis_complete()
