import pytest

APP_NAME = "overwrite analysis"


@pytest.mark.parametrize("app_name", [APP_NAME])
@pytest.mark.parametrize(
    "analysis_data",
    [
        {
            APP_NAME: {"options": {"target": ["eap8"]}},
        },
    ],
)
@pytest.mark.parametrize("ide", ["vscode"])
@pytest.mark.vscode
def test_overwrite_option(setup_vscode, configurations, app_name, analysis_data, ide):
    # Automates polarion MTA-481
    pytest.skip("Overwrite option is disabled")
    vscode = setup_vscode
    vscode.set_focus()

    vscode.run_simple_analysis(app_name)
    assert vscode.is_analysis_complete()

    configurations_object, _, _ = configurations
    running_configuration = configurations_object.configurations[0]
    running_configuration.options.overwrite = True

    vscode.update_configuration(running_configuration)

    vscode.clear_terminal_output_panel()
    vscode.run_simple_analysis(app_name)
    assert vscode.is_analysis_complete()
