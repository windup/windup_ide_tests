import pytest

from src.models.configuration.configuration import Configuration
from src.models.configuration.summery import Summary


@pytest.mark.parametrize("app_name", ["classifications check"])
@pytest.mark.parametrize(
    "analysis_data",
    [
        {
            "classifications check": {"options": {"target": ["eap8"]}},
        },
    ],
)
@pytest.mark.parametrize("ide", ["vscode"])
@pytest.mark.vscode
def test_no_generated_classifications(setup_vscode, configurations, app_name, analysis_data, ide):
    # Automates polarion MTA-503
    vscode = setup_vscode
    vscode.set_focus()
    vscode.open_mta_perspective()
    vscode.run_simple_analysis(app_name)
    status, message = vscode.is_analysis_complete()
    assert status, message

    configuration: Configuration = vscode.configurations_object.get_configuration(app_name)
    analysis_summery: Summary = configuration.summary

    assert analysis_summery.classification_count == 0, f"{str(analysis_summery.classification_count)} classifications were generated"


@pytest.mark.parametrize("app_name", ["quickfixes check"])
@pytest.mark.parametrize(
    "analysis_data",
    [
        {
            "quickfixes check": {"options": {"target": ["eap8"]}},
        },
    ],
)
@pytest.mark.parametrize("ide", ["vscode"])
@pytest.mark.vscode
def test_no_quickfixes_generated(setup_vscode, configurations, app_name, analysis_data, ide):
    # Automates polarion MTA-513
    vscode = setup_vscode
    vscode.set_focus()
    vscode.open_mta_perspective()
    vscode.run_simple_analysis(app_name)
    status, message = vscode.is_analysis_complete()
    assert status, message

    configuration: Configuration = vscode.configurations_object.get_configuration(app_name)
    analysis_summery: Summary = configuration.summary

    assert analysis_summery.quickfixes == {}, f"quickfixes were generated: {analysis_summery.quickfixes}"
