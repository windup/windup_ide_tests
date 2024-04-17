import pytest

APP_NAME = "analyze known libraries"


@pytest.mark.parametrize("app_name", [APP_NAME])
@pytest.mark.parametrize(
    "analysis_data",
    [
        {
            APP_NAME: {"options": {"target": ["eap8"], "analyze-known-libraries": True}},
        },
    ],
)
@pytest.mark.parametrize("ide", ["vscode"])
@pytest.mark.vscode
def test_analyze_known_libraries_option(setup_vscode, configurations, app_name, analysis_data, ide):
    # Automates polarion MTA-494
    vscode = setup_vscode
    vscode.set_focus()
    vscode.run_simple_analysis(app_name)
    assert vscode.is_analysis_complete()
