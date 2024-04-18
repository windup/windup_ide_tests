import pytest

APP_NAME = "selected sources"


@pytest.mark.parametrize("app_name", [APP_NAME])
@pytest.mark.parametrize(
    "analysis_data",
    [
        {
            APP_NAME: {"options": {"source": ["agroal", "amazon", "avro", "camel", "drools", "eapxp", "glassfish", "jakarta", "jsonb", "logging", "flyway"]}},
        },
    ],
)
@pytest.mark.parametrize("ide", ["vscode"])
@pytest.mark.vscode
def test_mta_485_selected_sources(setup_vscode, configurations, app_name, analysis_data, ide):
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
