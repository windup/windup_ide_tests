import pytest

from src.models.configuration.configurations_object import ConfigurationsObject


@pytest.mark.parametrize("app_name", ["source mode option"])
@pytest.mark.parametrize(
    "analysis_data",
    [
        {
            "cancel analysis": {"options": {"target": ["eap8"]}},
        },
    ],
)
@pytest.mark.parametrize("ide", ["vscode"])
@pytest.mark.vscode
def test_delete_configuration(setup_vscode, configurations, app_name, analysis_data, ide):
    # Automates Polarion MTA-483

    vscode = setup_vscode
    vscode.set_focus()
    vscode.refresh_configuration()
    model_file_path = vscode.get_model_file_path()
    configurations_object = ConfigurationsObject()
    conf_object = configurations_object.get_model_object(model_file_path)
    assert str(conf_object.configurations[0].options.source_mode) == str(True)
    assert conf_object.configurations[0].options.mode == "source-only"
