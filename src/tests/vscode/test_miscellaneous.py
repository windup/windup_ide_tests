import pytest

DELETE_CONFIG = [
    {
        "delete configuration": {"options": {"target": ["eap7"]}},
    },
]

SELECTED_TARGETS_CONFIG = [
    {
        "selected targets": {"options": {"target": ["azure-appservice", "camel", "containerization", "eap", "eap7", "eap8", "jakarta-ee", "jakarta-ee8+", "jakarta-ee9+", "jwst6", "springboot"]}},
    },
]

SELECTED_SOURCES_CONFIG = [
    {
        "selected sources": {"options": {"source": ["agroal", "amazon", "avro", "camel", "drools", "eapxp", "glassfish", "jakarta", "jsonb", "logging", "flyway"]}},
    },
]


@pytest.mark.parametrize("app_name", ["delete configuration"])
@pytest.mark.parametrize("analysis_data", DELETE_CONFIG)
@pytest.mark.parametrize("ide", ["vscode"])
@pytest.mark.vscode
def test_delete_configuration(setup_vscode, vscode_config, configurations, app_name, analysis_data, ide):
    # Automates Polarion MTA-498

    vscode = setup_vscode
    vscode.set_focus()
    vscode.refresh_configuration()
    vscode.delete_configuration(app_name)
    model_json_path = f"{vscode_config['plugin_cache_path']}/model.json"
    configurations_object = vscode.get_configurations_list_from_model_file(model_json_path)
    found_configurations = [config for config in configurations_object.configurations if config.name == app_name]
    assert len(found_configurations) == 0, "Configuration not removed from model.json"


@pytest.mark.parametrize("app_name", ["selected targets"])
@pytest.mark.parametrize("analysis_data", SELECTED_TARGETS_CONFIG)
@pytest.mark.parametrize("ide", ["vscode"])
@pytest.mark.vscode
def test_selected_targets(setup_vscode, configurations, app_name, analysis_data, ide):
    # Automates Polarion MTA-474

    vscode = setup_vscode
    vscode.set_focus()
    vscode.refresh_configuration()
    vscode.run_simple_analysis(app_name)
    vscode.cancel_analysis()
    command_map = vscode.fetch_executed_cli_command_map()
    configurations_object, _, _ = configurations

    inserted_targets = configurations_object.configurations[0].options.target
    picked_targets = command_map["target"]
    assert set(inserted_targets) == set(picked_targets), f"Some targets were not picked by the UI: {[tgt for tgt in inserted_targets if tgt not in picked_targets]}"


@pytest.mark.parametrize("app_name", ["selected sources"])
@pytest.mark.parametrize("analysis_data", SELECTED_SOURCES_CONFIG)
@pytest.mark.parametrize("ide", ["vscode"])
@pytest.mark.vscode
def test_selected_sources(setup_vscode, configurations, app_name, analysis_data, ide):
    # Automates Polarion MTA-485

    vscode = setup_vscode
    vscode.set_focus()
    vscode.refresh_configuration()
    vscode.run_simple_analysis(app_name)
    vscode.cancel_analysis()
    command_map = vscode.fetch_executed_cli_command_map()
    configurations_object, _, _ = configurations

    inserted_sources = configurations_object.configurations[0].options.source
    picked_sources = command_map["source"]
    assert set(inserted_sources) == set(picked_sources), f"Some sources were not picked by the UI: {[tgt for tgt in inserted_sources if tgt not in picked_sources]}"
