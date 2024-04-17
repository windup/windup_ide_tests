import pytest

APP_NAME = "selected targets"


@pytest.mark.parametrize("app_name", [APP_NAME])
@pytest.mark.parametrize(
    "analysis_data",
    [
        {
            APP_NAME: {"options": {"target": ["azure-appservice", "camel", "containerization", "eap", "eap7", "eap8", "jakarta-ee", "jakarta-ee8+", "jakarta-ee9+", "jwst6", "springboot"]}},
        },
    ],
)
@pytest.mark.parametrize("ide", ["vscode"])
@pytest.mark.vscode
def test_mta_474_selected_targets(setup_vscode, configurations, app_name, analysis_data, ide):
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
