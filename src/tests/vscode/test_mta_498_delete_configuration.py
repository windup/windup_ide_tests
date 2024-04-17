import pytest

APP_NAME = "delete configuration"


@pytest.mark.parametrize("app_name", [APP_NAME])
@pytest.mark.parametrize(
    "analysis_data",
    [
        {
            APP_NAME: {"options": {"target": ["eap7"]}},
        },
    ],
)
@pytest.mark.parametrize("ide", ["vscode"])
@pytest.mark.vscode
def test_mta_498_delete_configuration(setup_vscode, vscode_config, configurations, app_name, analysis_data, ide):
    # Automates Polarion MTA-498

    vscode = setup_vscode
    vscode.set_focus()
    vscode.refresh_configuration()
    vscode.delete_configuration(app_name)
    model_json_path = f"{vscode_config['plugin_cache_path']}/model.json"
    configurations_object = vscode.get_configurations_list_from_model_file(model_json_path)
    found_configurations = [config for config in configurations_object.configurations if config.name == app_name]
    assert len(found_configurations) == 0, "Configuration not removed from model.json"
